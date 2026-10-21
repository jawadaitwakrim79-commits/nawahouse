from __future__ import annotations
import logging
from datetime import datetime, timezone, timedelta

from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy import select, func, text
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.models.models import Order, OrderItem
from app.schemas.schemas import OrderIn, OrderOut, FORBIDDEN_PURCHASE_EVENTS
from app.core.phone import normalize_sa_phone, PhoneError
from app.core.pricing import main_total, order_total
from app.services.orders import build_sheet_payload, get_client_ip
from app.services.sheets import send_to_sheet
from app.services.capi import send_purchase_capi

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/orders", response_model=OrderOut, status_code=status.HTTP_201_CREATED)
async def create_order(
    body: OrderIn,
    request: Request,
    db: AsyncSession = Depends(get_db),
) -> OrderOut:
    # --- Idempotency: return existing if event_id already committed ---
    existing = await db.scalar(
        select(Order).where(Order.client_event_id == body.event_id)
    )
    if existing:
        return OrderOut(
            order_id=existing.public_id,
            event_id=existing.client_event_id,
            total_sar=existing.total_sar,
        )

    # --- Rate limit: max 3 successful orders per phone per 24h ---
    try:
        phone = normalize_sa_phone(body.phone)
    except PhoneError as exc:
        raise HTTPException(status_code=422, detail=str(exc))

    since = datetime.now(timezone.utc) - timedelta(hours=24)
    recent_count = await db.scalar(
        select(func.count()).select_from(Order).where(
            Order.phone_e164 == phone.e164,
            Order.created_at >= since,
        )
    )
    if (recent_count or 0) >= 3:
        raise HTTPException(status_code=429, detail="Too many orders for this number today")

    # --- Price computation ---
    main_lines = [l for l in body.lines if l.pricing == "main"]
    upsell_lines = [l for l in body.lines if l.pricing == "upsell"]
    main_units = sum(l.quantity for l in main_lines)
    upsell_units = len(upsell_lines)
    upsell_slug = upsell_lines[0].slug if upsell_lines else None
    total = order_total(main_units, upsell_units)

    # --- Build public_id from sequence ---
    seq_val = await db.scalar(text("SELECT nextval('order_public_seq')"))
    public_id = f"NAW-{seq_val}"

    client_ip = get_client_ip(request)
    user_agent = request.headers.get("User-Agent", "")

    order = Order(
        public_id=public_id,
        client_event_id=body.event_id,
        customer_name=body.name.strip(),
        phone_e164=phone.e164,
        main_units=main_units,
        upsell_slug=upsell_slug,
        total_sar=total,
        status="new",
        sheet_status="pending",
        page_url=body.page_url,
        client_ip=client_ip,
        user_agent=user_agent,
        fbp=body.fbp,
        fbc=body.fbc,
        ttp=body.ttp,
        ttclid=body.ttclid,
        sc_click_id=body.sc_click_id,
        external_id=body.external_id,
    )
    db.add(order)
    await db.flush()  # get the order.id

    for line in body.lines:
        db.add(OrderItem(
            order_id=order.id,
            slug=line.slug,
            quantity=line.quantity,
            pricing=line.pricing,
        ))

    await db.commit()
    await db.refresh(order)

    # --- Sheet (fire and forget, don't block the response) ---
    sheet_payload = build_sheet_payload(order, body, phone, client_ip, user_agent)
    sheet_ok = await send_to_sheet(sheet_payload)
    order.sheet_status = "sent" if sheet_ok else "failed"
    await db.commit()

    # --- CAPI ---
    event_source_url = body.event_source_url or f"https://nawahouse.shop/thank-you?order={public_id}"
    await send_purchase_capi(
        order=order,
        items=body.lines,
        event_id=body.event_id,
        event_source_url=event_source_url,
        client_ip=client_ip,
        user_agent=user_agent,
        db=db,
    )

    return OrderOut(order_id=public_id, event_id=body.event_id, total_sar=total)

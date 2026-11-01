from __future__ import annotations
import logging
from datetime import datetime, timezone, timedelta

from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy import select, func, text
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.models.models import Order, OrderItem
from app.schemas.schemas import OrderIn, OrderOut
from app.core.phone import normalize_ma_phone, PhoneError
from app.core.pricing import goods_total, order_total
from app.services.orders import build_sheet_payload, get_client_ip
from app.services.sheets import send_to_sheet
from app.services.capi import send_purchase_capi
from app.services.ip_intel import IpIntel, lookup as lookup_ip
from app.services.settings_store import get_shipping_mad

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/orders", response_model=OrderOut, status_code=status.HTTP_201_CREATED)
async def create_order(
    body: OrderIn,
    request: Request,
    db: AsyncSession = Depends(get_db),
) -> OrderOut:
    # Country is recorded for the dashboard. It does not reject the order.
    client_ip = get_client_ip(request)
    try:
        intel = await lookup_ip(client_ip)
    except Exception as exc:
        logger.error("ip lookup failed: %s", type(exc).__name__)
        intel = IpIntel.unknown(source="error")
    logger.info(
        "order decision=allowed country=%s source=%s",
        intel.country_code,
        intel.source,
    )

    existing = await db.scalar(
        select(Order).where(Order.client_event_id == body.event_id)
    )
    if existing:
        return OrderOut(
            order_id=existing.public_id,
            event_id=existing.client_event_id,
            total_mad=existing.total_mad,
            shipping_mad=existing.shipping_mad or 0,
        )

    try:
        phone = normalize_ma_phone(body.phone)
    except PhoneError as exc:
        raise HTTPException(status_code=422, detail="رقم الهاتف المغربي غير صالح.") from exc

    since = datetime.now(timezone.utc) - timedelta(hours=24)
    recent_count = await db.scalar(
        select(func.count()).select_from(Order).where(
            Order.phone_e164 == phone.e164,
            Order.created_at >= since,
        )
    )
    if (recent_count or 0) >= 3:
        raise HTTPException(status_code=429, detail="Too many orders for this number today")

    shipping = await get_shipping_mad(db)
    goods = goods_total([(line.slug, line.quantity) for line in body.lines])
    total = order_total(goods, shipping)
    main_units = sum(line.quantity for line in body.lines)

    seq_val = await db.scalar(text("SELECT nextval('order_public_seq')"))
    public_id = f"NAW-{seq_val}"
    user_agent = request.headers.get("User-Agent", "")

    order = Order(
        public_id=public_id,
        client_event_id=body.event_id,
        customer_name=body.name.strip(),
        phone_e164=phone.e164,
        main_units=main_units,
        upsell_slug=None,
        total_mad=total,
        shipping_mad=shipping,
        city=body.city,
        address=body.address,
        delivery_notes=body.delivery_notes,
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
    await db.flush()

    for line in body.lines:
        db.add(OrderItem(
            order_id=order.id,
            slug=line.slug,
            quantity=line.quantity,
            pricing=line.pricing,
            variant=line.variant,
        ))

    await db.commit()
    await db.refresh(order)

    sheet_payload = build_sheet_payload(order, body, phone, client_ip, user_agent)
    sheet_ok = await send_to_sheet(sheet_payload)
    order.sheet_status = "sent" if sheet_ok else "failed"
    await db.commit()

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

    return OrderOut(
        order_id=public_id,
        event_id=body.event_id,
        total_mad=total,
        shipping_mad=shipping,
    )

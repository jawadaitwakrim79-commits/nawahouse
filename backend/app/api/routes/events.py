from __future__ import annotations
import logging

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.schemas.schemas import EventIn, FORBIDDEN_PURCHASE_EVENTS
from app.services.orders import get_client_ip
from app.services.capi import send_funnel_capi

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/events", status_code=200)
async def track_event(
    body: EventIn,
    request: Request,
    db: AsyncSession = Depends(get_db),
) -> dict:
    if body.event_name in FORBIDDEN_PURCHASE_EVENTS:
        raise HTTPException(
            status_code=422,
            detail="Purchase events must be sent via /api/orders, not /api/events",
        )

    client_ip = get_client_ip(request)
    user_agent = request.headers.get("User-Agent", "")

    await send_funnel_capi(
        event_name=body.event_name,
        event_id=body.event_id,
        page_url=body.page_url,
        value=body.value,
        currency=body.currency or "SAR",
        content_ids=body.content_ids or [],
        phone=body.phone,
        external_id=body.external_id,
        fbp=body.fbp,
        fbc=body.fbc,
        ttp=body.ttp,
        ttclid=body.ttclid,
        sc_click_id=body.sc_click_id,
        client_ip=client_ip,
        user_agent=user_agent,
        db=db,
    )

    return {"ok": True}

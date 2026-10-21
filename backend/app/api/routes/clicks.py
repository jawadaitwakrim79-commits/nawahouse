from __future__ import annotations
import logging

from fastapi import APIRouter, Depends, Request
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.models.click import PageClick
from app.services.orders import get_client_ip
from app.services.ip_intel import lookup as lookup_ip

router = APIRouter()
logger = logging.getLogger(__name__)


class ClickIn(BaseModel):
    session_id: str = Field(..., max_length=64)
    path: str = Field(..., max_length=512)
    referrer: str | None = Field(None, max_length=1024)
    utm_source: str | None = Field(None, max_length=128)
    utm_medium: str | None = Field(None, max_length=128)
    utm_campaign: str | None = Field(None, max_length=256)
    fbclid: str | None = Field(None, max_length=256)
    ttclid: str | None = Field(None, max_length=256)
    sc_click_id: str | None = Field(None, max_length=256)


@router.post("/track-click", status_code=204)
async def track_click(
    body: ClickIn,
    request: Request,
    db: AsyncSession = Depends(get_db),
):
    """
    Record one page view with IP intelligence.
    Always returns 204 — never let analytics failures block user flows.
    """
    client_ip = get_client_ip(request)
    user_agent = request.headers.get("User-Agent", "")[:1024]

    try:
        intel = await lookup_ip(client_ip)
    except Exception as e:
        logger.warning("ip_intel lookup failed: %s", e)
        from app.services.ip_intel import IpIntel
        intel = IpIntel.unknown(source="error")

    click = PageClick(
        session_id=body.session_id,
        path=body.path[:512],
        referrer=(body.referrer or "")[:1024] or None,
        utm_source=body.utm_source,
        utm_medium=body.utm_medium,
        utm_campaign=body.utm_campaign,
        fbclid=body.fbclid,
        ttclid=body.ttclid,
        sc_click_id=body.sc_click_id,
        client_ip=client_ip or None,
        user_agent=user_agent or None,
        country_code=intel.country_code,
        is_vpn=intel.is_vpn,
        is_valid_ksa=intel.is_valid_ksa,
        intel_source=intel.source,
        risk_score=intel.risk_score,
    )
    db.add(click)
    try:
        await db.commit()
    except Exception as e:  # pragma: no cover
        logger.warning("click insert failed: %s", e)
        await db.rollback()
    return None

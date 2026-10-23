"""JSON admin API used by the website dashboard. Reads the live database."""
from __future__ import annotations

import logging
from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.admin.auth import admin_configured, credentials_are_valid, issue_session, require_admin
from app.admin.queries import (
    RIYADH_TZ,
    compute_metrics,
    daily_series,
    get_order,
    list_orders,
    parse_date_range,
    top_products,
)
from app.db.session import get_db
from app.models.models import Order

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/admin", tags=["admin-api"])


class LoginIn(BaseModel):
    token: str | None = None
    username: str | None = None
    password: str | None = None


def order_dict(order: Order) -> dict:
    created = order.created_at
    return {
        "public_id": order.public_id,
        "customer_name": order.customer_name,
        "phone_e164": order.phone_e164,
        "total_sar": order.total_sar,
        "status": order.status,
        "sheet_status": order.sheet_status,
        "main_units": order.main_units,
        "upsell_slug": order.upsell_slug,
        "page_url": order.page_url,
        "client_ip": order.client_ip,
        "client_event_id": order.client_event_id,
        "created_at": created.isoformat() if created else None,
        "items": [
            {"slug": item.slug, "quantity": item.quantity, "pricing": item.pricing}
            for item in (order.items or [])
        ],
    }


def _range_labels(date_from, date_to) -> tuple[str, str]:
    start = date_from.astimezone(RIYADH_TZ).strftime("%Y-%m-%d")
    end = (date_to - timedelta(days=1)).astimezone(RIYADH_TZ).strftime("%Y-%m-%d")
    return start, end


@router.post("/login")
async def login(body: LoginIn) -> dict:
    if not admin_configured():
        raise HTTPException(
            status_code=503,
            detail="Admin dashboard is not configured (set ADMIN_TOKEN, or ADMIN_USERNAME and ADMIN_PASSWORD)",
        )
    if not credentials_are_valid(body.token, body.username, body.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"ok": True, "session": issue_session()}


@router.get("/overview")
async def overview(
    date_from: str | None = Query(None, alias="from"),
    date_to: str | None = Query(None, alias="to"),
    include_invalid: bool = Query(False),
    db: AsyncSession = Depends(get_db),
    _user: str = Depends(require_admin),
) -> dict:
    start, end = parse_date_range(date_from, date_to)
    try:
        metrics = await compute_metrics(db, start, end, include_invalid=include_invalid)
        series = await daily_series(db, start, end)
        products = await top_products(db, start, end)
        recent = await list_orders(db, start, end, limit=20)
    except Exception as exc:
        logger.error("admin overview failed: %s", type(exc).__name__)
        raise HTTPException(status_code=500, detail="Could not read store data") from None
    label_from, label_to = _range_labels(start, end)
    return {
        "from": label_from,
        "to": label_to,
        "orders_count": metrics.orders_count,
        "orders_revenue": metrics.orders_revenue,
        "conversion_rate": metrics.conversion_rate,
        "total_clicks": metrics.total_clicks,
        "valid_ksa_clicks": metrics.valid_ksa_clicks,
        "vpn_clicks": metrics.vpn_clicks,
        "foreign_clicks": metrics.foreign_clicks,
        "unique_sessions": metrics.unique_sessions,
        "series": series,
        "top_products": products,
        "orders": [order_dict(order) for order in recent],
    }


@router.get("/orders")
async def orders(
    date_from: str | None = Query(None, alias="from"),
    date_to: str | None = Query(None, alias="to"),
    status: str | None = Query(None),
    page: int = Query(1, ge=1),
    db: AsyncSession = Depends(get_db),
    _user: str = Depends(require_admin),
) -> dict:
    start, end = parse_date_range(date_from, date_to)
    limit = 50
    offset = (page - 1) * limit
    try:
        rows = await list_orders(
            db, start, end, status_filter=status or None, limit=limit, offset=offset
        )
    except Exception as exc:
        logger.error("admin orders failed: %s", type(exc).__name__)
        raise HTTPException(status_code=500, detail="Could not read store data") from None
    label_from, label_to = _range_labels(start, end)
    return {
        "from": label_from,
        "to": label_to,
        "page": page,
        "orders": [order_dict(order) for order in rows],
    }


@router.get("/orders/{public_id}")
async def order_detail(
    public_id: str,
    db: AsyncSession = Depends(get_db),
    _user: str = Depends(require_admin),
) -> dict:
    try:
        order = await get_order(db, public_id)
    except Exception as exc:
        logger.error("admin order detail failed: %s", type(exc).__name__)
        raise HTTPException(status_code=500, detail="Could not read store data") from None
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return {"order": order_dict(order)}

from __future__ import annotations
from datetime import timedelta
from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException, Query, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession

from app.admin.auth import require_admin
from app.admin.queries import (
    RIYADH_TZ,
    compute_metrics,
    daily_series,
    get_order,
    list_orders,
    parse_date_range,
    top_products,
)
from app.core.config import settings
from app.db.session import get_db

router = APIRouter(prefix="/admin", tags=["admin"])

TEMPLATES_DIR = Path(__file__).parent / "templates"
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))


def _ctx_base(request: Request, _user: str) -> dict:
    return {
        "request": request,
        "admin_user": _user,
        "strict_ksa_only": settings.STRICT_KSA_ONLY,
        "vpn_provider": settings.VPN_PROVIDER or "—",
        "maxmind_configured": bool(
            settings.MAXMIND_DB_PATH
            or (settings.MAXMIND_ACCOUNT_ID and settings.MAXMIND_LICENSE_KEY)
        ),
    }


# ───────────────────────── Dashboard ─────────────────────────────────────────


@router.get("", response_class=HTMLResponse, include_in_schema=False)
@router.get("/", response_class=HTMLResponse, include_in_schema=False)
async def dashboard(
    request: Request,
    date_from: str | None = Query(None, alias="from"),
    date_to: str | None = Query(None, alias="to"),
    include_invalid: bool = Query(False),
    db: AsyncSession = Depends(get_db),
    user: str = Depends(require_admin),
):
    df, dt = parse_date_range(date_from, date_to)
    metrics = await compute_metrics(db, df, dt, include_invalid=include_invalid)
    series = await daily_series(db, df, dt)
    top = await top_products(db, df, dt)
    recent = await list_orders(db, df, dt, limit=10)

    ctx = _ctx_base(request, user)
    ctx.update({
        "m": metrics,
        "series": series,
        "top": top,
        "recent": recent,
        "from": df.astimezone(RIYADH_TZ).strftime("%Y-%m-%d"),
        "to": (dt - timedelta(days=1)).astimezone(RIYADH_TZ).strftime("%Y-%m-%d"),
        "include_invalid": include_invalid,
    })
    return templates.TemplateResponse("dashboard.html", ctx)


# ───────────────────────── Orders list ───────────────────────────────────────


@router.get("/orders", response_class=HTMLResponse, include_in_schema=False)
async def orders_list(
    request: Request,
    date_from: str | None = Query(None, alias="from"),
    date_to: str | None = Query(None, alias="to"),
    status: str | None = Query(None),
    page: int = Query(1, ge=1),
    db: AsyncSession = Depends(get_db),
    user: str = Depends(require_admin),
):
    df, dt = parse_date_range(date_from, date_to)
    limit = 50
    offset = (page - 1) * limit
    orders = await list_orders(db, df, dt, status_filter=status, limit=limit, offset=offset)

    ctx = _ctx_base(request, user)
    ctx.update({
        "orders": orders,
        "page": page,
        "status": status or "",
        "from": df.astimezone(RIYADH_TZ).strftime("%Y-%m-%d"),
        "to": (dt - timedelta(days=1)).astimezone(RIYADH_TZ).strftime("%Y-%m-%d"),
    })
    return templates.TemplateResponse("orders.html", ctx)


# ───────────────────────── Order detail ──────────────────────────────────────


@router.get("/orders/{public_id}", response_class=HTMLResponse, include_in_schema=False)
async def order_detail(
    request: Request,
    public_id: str,
    db: AsyncSession = Depends(get_db),
    user: str = Depends(require_admin),
):
    order = await get_order(db, public_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    ctx = _ctx_base(request, user)
    ctx.update({"o": order})
    return templates.TemplateResponse("order_detail.html", ctx)


# ───────────────────────── JSON APIs (for chart) ─────────────────────────────


@router.get("/api/series", include_in_schema=False)
async def api_series(
    date_from: str | None = Query(None, alias="from"),
    date_to: str | None = Query(None, alias="to"),
    db: AsyncSession = Depends(get_db),
    _user: str = Depends(require_admin),
):
    df, dt = parse_date_range(date_from, date_to)
    return {"series": await daily_series(db, df, dt)}

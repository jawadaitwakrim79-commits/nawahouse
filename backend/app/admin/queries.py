from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Optional

from sqlalchemy import and_, case, func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.click import PageClick
from app.models.models import Order, OrderItem


# Morocco uses UTC+1. A fixed offset avoids a tzdata package in the slim image.
STORE_TZ = timezone(timedelta(hours=1))
RIYADH_TZ = STORE_TZ


def parse_date_range(
    from_str: str | None,
    to_str: str | None,
) -> tuple[datetime, datetime]:
    """Parse YYYY-MM-DD in Africa/Casablanca into a UTC range [from, to)."""
    now_local = datetime.now(STORE_TZ)
    today_local = now_local.replace(hour=0, minute=0, second=0, microsecond=0)
    default_to = today_local + timedelta(days=1)
    default_from = today_local - timedelta(days=29)

    def _p(value: str, fallback: datetime) -> datetime:
        try:
            parsed = datetime.strptime(value, "%Y-%m-%d")
            return parsed.replace(tzinfo=STORE_TZ)
        except Exception:
            return fallback

    date_from = _p(from_str, default_from) if from_str else default_from
    date_to = _p(to_str, default_to) if to_str else default_to
    return date_from.astimezone(timezone.utc), date_to.astimezone(timezone.utc)


@dataclass
class Metrics:
    date_from: datetime
    date_to: datetime
    total_clicks: int
    valid_ksa_clicks: int
    vpn_clicks: int
    foreign_clicks: int
    unique_sessions: int
    orders_count: int
    orders_revenue: int  # in MAD
    conversion_rate: float  # orders / all clicks
    morocco_clicks: int = 0


def _apply_valid_ksa_filter(stmt, include_invalid: bool):
    """Country is not a gate. Every visit is counted."""
    del include_invalid
    return stmt


async def compute_metrics(
    db: AsyncSession,
    date_from: datetime,
    date_to: datetime,
    include_invalid: bool = False,
) -> Metrics:
    # Aggregates (sum of boolean matches via CASE)
    agg_stmt = select(
        func.count(PageClick.id).label("total"),
        func.sum(case((PageClick.is_valid_ksa.is_(True), 1), else_=0)).label("valid"),
        func.sum(case((PageClick.is_vpn.is_(True), 1), else_=0)).label("vpn"),
        func.sum(case((PageClick.country_code == "MA", 1), else_=0)).label("morocco"),
        func.sum(
            case(
                (and_(PageClick.country_code.is_not(None), PageClick.country_code != "MA"), 1),
                else_=0,
            )
        ).label("foreign"),
        func.count(func.distinct(PageClick.session_id)).label("sessions"),
    ).where(
        PageClick.created_at >= date_from,
        PageClick.created_at < date_to,
    )

    row = (await db.execute(agg_stmt)).one()
    total = int(row.total or 0)
    valid = int(row.valid or 0)
    vpn = int(row.vpn or 0)
    morocco = int(row.morocco or 0)
    foreign = int(row.foreign or 0)
    sessions = int(row.sessions or 0)

    # Orders
    orders_stmt = select(
        func.count(Order.id).label("count"),
        func.coalesce(func.sum(Order.total_mad), 0).label("rev"),
    ).where(
        Order.created_at >= date_from,
        Order.created_at < date_to,
    )
    o_row = (await db.execute(orders_stmt)).one()
    orders_count = int(o_row.count or 0)
    orders_rev = int(o_row.rev or 0)

    denom = total
    cvr = (orders_count / denom) if denom > 0 else 0.0

    return Metrics(
        date_from=date_from,
        date_to=date_to,
        total_clicks=total,
        valid_ksa_clicks=valid,
        vpn_clicks=vpn,
        foreign_clicks=foreign,
        unique_sessions=sessions,
        orders_count=orders_count,
        orders_revenue=orders_rev,
        conversion_rate=cvr,
        morocco_clicks=morocco,
    )


async def daily_series(
    db: AsyncSession, date_from: datetime, date_to: datetime
) -> list[dict]:
    """Daily breakdown of valid clicks + orders, for the chart."""
    clicks_stmt = (
        select(
            func.date_trunc("day", PageClick.created_at).label("d"),
            func.count(PageClick.id).label("valid"),
        )
        .where(PageClick.created_at >= date_from, PageClick.created_at < date_to)
        .group_by("d")
        .order_by("d")
    )
    rows_c = (await db.execute(clicks_stmt)).all()
    by_day = {r.d.date().isoformat(): {"date": r.d.date().isoformat(), "clicks": int(r.valid or 0), "orders": 0}
              for r in rows_c}

    orders_stmt = (
        select(
            func.date_trunc("day", Order.created_at).label("d"),
            func.count(Order.id).label("c"),
        )
        .where(Order.created_at >= date_from, Order.created_at < date_to)
        .group_by("d")
        .order_by("d")
    )
    rows_o = (await db.execute(orders_stmt)).all()
    for r in rows_o:
        key = r.d.date().isoformat()
        node = by_day.setdefault(key, {"date": key, "clicks": 0, "orders": 0})
        node["orders"] = int(r.c or 0)

    return sorted(by_day.values(), key=lambda x: x["date"])


async def list_orders(
    db: AsyncSession,
    date_from: datetime,
    date_to: datetime,
    status_filter: Optional[str] = None,
    limit: int = 100,
    offset: int = 0,
) -> list[Order]:
    stmt = (
        select(Order)
        .where(Order.created_at >= date_from, Order.created_at < date_to)
        .options(selectinload(Order.items))
        .order_by(Order.created_at.desc())
        .limit(limit)
        .offset(offset)
    )
    if status_filter:
        stmt = stmt.where(Order.status == status_filter)
    return list((await db.execute(stmt)).scalars().all())


async def get_order(db: AsyncSession, public_id: str) -> Optional[Order]:
    stmt = (
        select(Order)
        .where(Order.public_id == public_id)
        .options(selectinload(Order.items))
    )
    return (await db.execute(stmt)).scalar_one_or_none()


async def top_products(
    db: AsyncSession, date_from: datetime, date_to: datetime
) -> list[dict]:
    stmt = (
        select(
            OrderItem.slug,
            func.sum(OrderItem.quantity).label("qty"),
        )
        .join(Order, Order.id == OrderItem.order_id)
        .where(Order.created_at >= date_from, Order.created_at < date_to)
        .group_by(OrderItem.slug)
        .order_by(func.sum(OrderItem.quantity).desc())
    )
    rows = (await db.execute(stmt)).all()
    return [{"slug": r.slug, "qty": int(r.qty)} for r in rows]

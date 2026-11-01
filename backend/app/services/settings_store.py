"""Store settings persisted in Postgres. Shipping is never invented in code."""

from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.catalog import CATEGORIES
from app.models.models import Category, StoreSetting

SHIPPING_KEY = "shipping_mad"


async def get_shipping_mad(db: AsyncSession) -> int:
    value = await db.scalar(
        select(StoreSetting.value).where(StoreSetting.key == SHIPPING_KEY)
    )
    if value is None:
        return 0
    try:
        amount = int(value)
    except (TypeError, ValueError):
        return 0
    return amount if amount >= 0 else 0


async def set_shipping_mad(db: AsyncSession, amount: int) -> int:
    if amount < 0 or amount > 9999:
        raise ValueError("shipping must be between 0 and 9999")
    row = await db.get(StoreSetting, SHIPPING_KEY)
    if row is None:
        db.add(StoreSetting(key=SHIPPING_KEY, value=str(amount)))
    else:
        row.value = str(amount)
    await db.commit()
    return amount


async def list_categories(db: AsyncSession) -> list[dict]:
    rows = list(
        (await db.scalars(select(Category).order_by(Category.sort_order, Category.slug))).all()
    )
    if not rows:
        return [
            {
                "slug": category.slug,
                "name_ar": category.name_ar,
                "sort_order": category.sort_order,
                "active": True,
            }
            for category in CATEGORIES
        ]
    return [
        {
            "slug": row.slug,
            "name_ar": row.name_ar,
            "sort_order": row.sort_order,
            "active": row.active,
        }
        for row in rows
    ]


async def update_categories(db: AsyncSession, items: list[dict]) -> list[dict]:
    known = {category.slug for category in CATEGORIES}
    for item in items:
        slug = item["slug"]
        if slug not in known:
            raise ValueError(f"Unknown category: {slug}")
        row = await db.get(Category, slug)
        name = str(item["name_ar"]).strip()
        if len(name) < 2 or len(name) > 40:
            raise ValueError("category name must be 2–40 characters")
        if row is None:
            db.add(
                Category(
                    slug=slug,
                    name_ar=name,
                    sort_order=int(item.get("sort_order") or 0),
                    active=bool(item.get("active", True)),
                )
            )
        else:
            row.name_ar = name
            row.active = bool(item.get("active", True))
    await db.commit()
    return await list_categories(db)

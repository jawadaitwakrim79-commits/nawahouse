"""Public store config: currency, shipping, and categories."""

from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.services.settings_store import get_shipping_mad, list_categories

router = APIRouter()


@router.get("/store")
async def store_config(db: AsyncSession = Depends(get_db)) -> dict:
    return {
        "currency": "MAD",
        "shipping_mad": await get_shipping_mad(db),
        "categories": await list_categories(db),
    }

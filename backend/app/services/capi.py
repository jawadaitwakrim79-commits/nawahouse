"""
CAPI service — Meta, TikTok, and Snap.

Hashing rules (from docs/11-TRACKING-PIXELS-CAPI.md):
  Meta / Snap  phone: hash of "966XXXXXXXXX"  (no plus)
  TikTok       phone: hash of "+966XXXXXXXXX" (plus kept)
  country (Meta): hash of "sa"
  external_id: hash of trimmed UUID (Meta + TikTok)
  IP, UA, fbp, fbc, ttp, ttclid, sc_click_id: raw / never hash
"""

from __future__ import annotations
import asyncio
import logging
import time
from typing import Any

import httpx
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.hashing import maybe_hash, sha256
from app.core.phone import normalize_sa_phone, PhoneError
from app.models.models import Order, OrderItem, TrackingEvent
from app.schemas.schemas import OrderLineIn

logger = logging.getLogger(__name__)

PRODUCT_NAMES = {
    "oud": "نوا عود",
    "shafaq": "نوا شفق",
    "safa": "نوا صفاء",
}

TIKTOK_EVENT_MAP = {
    "Purchase": "CompletePayment",
    "PageView": "Pageview",
    "ViewContent": "ViewContent",
    "AddToCart": "AddToCart",
    "InitiateCheckout": "InitiateCheckout",
}

SNAP_EVENT_MAP = {
    "Purchase": "PURCHASE",
    "PageView": "PAGE_VIEW",
    "ViewContent": "VIEW_CONTENT",
    "AddToCart": "ADD_CART",
    "InitiateCheckout": "START_CHECKOUT",
}


async def _record_tracking(
    db: AsyncSession,
    event_id: str,
    event_name: str,
    platform: str,
    http_status: int | None,
    ok: bool,
) -> None:
    try:
        te = TrackingEvent(
            event_id=event_id,
            event_name=event_name,
            platform=platform,
            http_status=http_status,
            ok=ok,
        )
        db.add(te)
        await db.commit()
    except IntegrityError:
        await db.rollback()  # duplicate — idempotent, ignore


async def _send_meta(
    event_name: str,
    event_id: str,
    event_time: int,
    event_source_url: str,
    user_data: dict,
    custom_data: dict,
    db: AsyncSession,
) -> None:
    if not settings.META_PIXEL_ID or not settings.META_CAPI_ACCESS_TOKEN:
        return

    payload: dict[str, Any] = {
        "data": [
            {
                "event_name": event_name,
                "event_time": event_time,
                "event_id": event_id,
                "event_source_url": event_source_url,
                "action_source": "website",
                "user_data": {k: v for k, v in user_data.items() if v is not None},
                "custom_data": custom_data,
            }
        ]
    }
    if settings.META_TEST_EVENT_CODE:
        payload["test_event_code"] = settings.META_TEST_EVENT_CODE

    url = f"https://graph.facebook.com/v21.0/{settings.META_PIXEL_ID}/events"
    params = {"access_token": settings.META_CAPI_ACCESS_TOKEN}
    http_status, ok = None, False
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            r = await client.post(url, params=params, json=payload)
            http_status = r.status_code
            ok = r.status_code < 300
            if not ok:
                logger.warning("Meta CAPI %s: %s", r.status_code, r.text[:200])
    except Exception as exc:
        logger.error("Meta CAPI error: %s", exc)
    await _record_tracking(db, event_id, event_name, "meta", http_status, ok)


async def _send_tiktok(
    event_name: str,
    event_id: str,
    event_time: int,
    event_source_url: str,
    user_data: dict,
    properties: dict,
    db: AsyncSession,
) -> None:
    if not settings.TIKTOK_PIXEL_CODE or not settings.TIKTOK_ACCESS_TOKEN:
        return

    tt_event = TIKTOK_EVENT_MAP.get(event_name, event_name)
    data_item: dict[str, Any] = {
        "event": tt_event,
        "event_time": event_time,
        "event_id": event_id,
        "user": {k: v for k, v in user_data.items() if v is not None},
        "page": {"url": event_source_url},
        "properties": properties,
    }

    payload: dict[str, Any] = {
        "event_source": "web",
        "event_source_id": settings.TIKTOK_PIXEL_CODE,
        "data": [data_item],
    }
    if settings.TIKTOK_TEST_EVENT_CODE:
        payload["test_event_code"] = settings.TIKTOK_TEST_EVENT_CODE

    url = "https://business-api.tiktok.com/open_api/v1.3/event/track/"
    headers = {"Access-Token": settings.TIKTOK_ACCESS_TOKEN}
    http_status, ok = None, False
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            r = await client.post(url, headers=headers, json=payload)
            http_status = r.status_code
            ok = r.status_code < 300
            if not ok:
                logger.warning("TikTok CAPI %s: %s", r.status_code, r.text[:200])
    except Exception as exc:
        logger.error("TikTok CAPI error: %s", exc)
    await _record_tracking(db, event_id, tt_event, "tiktok", http_status, ok)


async def _send_snap(
    event_name: str,
    event_id: str,
    event_time: int,
    event_source_url: str,
    user_data: dict,
    custom_data: dict,
    db: AsyncSession,
) -> None:
    if not settings.SNAP_PIXEL_ID or not settings.SNAP_CAPI_ACCESS_TOKEN:
        return

    snap_event = SNAP_EVENT_MAP.get(event_name, event_name)
    data_item: dict[str, Any] = {
        "event_name": snap_event,
        "event_time": event_time,
        "event_id": event_id,
        "action_source": "WEB",
        "event_source_url": event_source_url,
        "user_data": {k: v for k, v in user_data.items() if v is not None},
        "custom_data": custom_data,
    }
    if settings.SNAP_TEST_EVENT_CODE:
        data_item["test_event_code"] = settings.SNAP_TEST_EVENT_CODE

    payload: dict[str, Any] = {"data": [data_item]}
    url = f"https://tr.snapchat.com/v3/{settings.SNAP_PIXEL_ID}/events"
    params = {"access_token": settings.SNAP_CAPI_ACCESS_TOKEN}
    http_status, ok = None, False
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            r = await client.post(url, params=params, json=payload)
            http_status = r.status_code
            ok = r.status_code < 300
            if not ok:
                logger.warning("Snap CAPI %s: %s", r.status_code, r.text[:200])
    except Exception as exc:
        logger.error("Snap CAPI error: %s", exc)
    await _record_tracking(db, event_id, snap_event, "snap", http_status, ok)


def _build_user_data(
    phone_e164: str | None,
    external_id: str | None,
    client_ip: str | None,
    user_agent: str | None,
    fbp: str | None,
    fbc: str | None,
    ttp: str | None,
    ttclid: str | None,
    sc_click_id: str | None,
    customer_name: str | None,
) -> tuple[dict, dict, dict]:
    """Return (meta_ud, tiktok_ud, snap_ud)."""
    # First name extraction for Meta
    first_name: str | None = None
    if customer_name:
        parts = customer_name.strip().split()
        if parts:
            first_name = parts[0].lower()

    meta_ph = snap_ph = tt_ph = None
    if phone_e164:
        meta_snap_digits = phone_e164.lstrip("+")  # "966512345678"
        meta_ph = [maybe_hash(meta_snap_digits)]
        snap_ph = [maybe_hash(meta_snap_digits)]
        tt_ph = [maybe_hash(phone_e164)]  # "+966512345678"

    ext_hash = maybe_hash(external_id.strip() if external_id else None)

    meta_ud: dict[str, Any] = {
        "ph": meta_ph,
        "fn": [sha256(first_name)] if first_name else None,
        "country": [sha256("sa")],
        "external_id": [ext_hash] if ext_hash else None,
        "client_ip_address": client_ip or None,
        "client_user_agent": user_agent or None,
        "fbp": fbp or None,
        "fbc": fbc or None,
    }

    tiktok_ud: dict[str, Any] = {
        "phone": tt_ph[0] if tt_ph else None,
        "external_id": ext_hash,
        "ip": client_ip or None,
        "user_agent": user_agent or None,
        "ttclid": ttclid or None,
        "ttp": ttp or None,
    }

    snap_ud: dict[str, Any] = {
        "ph": snap_ph,
        "client_ip_address": client_ip or None,
        "client_user_agent": user_agent or None,
        "sc_click_id": sc_click_id or None,
    }

    return meta_ud, tiktok_ud, snap_ud


async def send_purchase_capi(
    order: Order,
    items: list[OrderLineIn],
    event_id: str,
    event_source_url: str,
    client_ip: str,
    user_agent: str,
    db: AsyncSession,
) -> None:
    event_time = int(time.time())
    meta_ud, tiktok_ud, snap_ud = _build_user_data(
        phone_e164=order.phone_e164,
        external_id=order.external_id,
        client_ip=client_ip,
        user_agent=user_agent,
        fbp=order.fbp,
        fbc=order.fbc,
        ttp=order.ttp,
        ttclid=order.ttclid,
        sc_click_id=order.sc_click_id,
        customer_name=order.customer_name,
    )

    content_ids = list({l.slug for l in items})
    num_items = sum(l.quantity for l in items)
    total = order.total_sar

    meta_contents = [
        {
            "id": l.slug,
            "quantity": l.quantity,
            "item_price": 99 if l.pricing == "upsell" else 199,
        }
        for l in items
    ]
    tt_contents = [
        {
            "content_id": l.slug,
            "content_name": PRODUCT_NAMES.get(l.slug, l.slug),
            "quantity": l.quantity,
            "price": 99 if l.pricing == "upsell" else 199,
            "brand": "Nawa House",
        }
        for l in items
    ]

    meta_custom = {
        "currency": "SAR",
        "value": total,
        "content_ids": content_ids,
        "content_type": "product",
        "contents": meta_contents,
        "num_items": num_items,
        "order_id": order.public_id,
    }
    tt_props = {
        "currency": "SAR",
        "value": float(total),
        "content_type": "product",
        "contents": tt_contents,
    }
    snap_custom = {
        "currency": "SAR",
        "value": total,
        "order_id": order.public_id,
        "content_ids": content_ids,
        "num_items": num_items,
    }

    await asyncio.gather(
        _send_meta("Purchase", event_id, event_time, event_source_url, meta_ud, meta_custom, db),
        _send_tiktok("Purchase", event_id, event_time, event_source_url, tiktok_ud, tt_props, db),
        _send_snap("Purchase", event_id, event_time, event_source_url, snap_ud, snap_custom, db),
        return_exceptions=True,
    )


async def send_funnel_capi(
    event_name: str,
    event_id: str,
    page_url: str | None,
    value: float | None,
    currency: str,
    content_ids: list[str],
    phone: str | None,
    external_id: str | None,
    fbp: str | None,
    fbc: str | None,
    ttp: str | None,
    ttclid: str | None,
    sc_click_id: str | None,
    client_ip: str,
    user_agent: str,
    db: AsyncSession,
) -> None:
    # Normalize phone if present
    phone_e164: str | None = None
    if phone:
        try:
            r = normalize_sa_phone(phone)
            phone_e164 = r.e164
        except PhoneError:
            phone_e164 = None

    event_time = int(time.time())
    event_src = page_url or "https://nawahouse.shop"

    meta_ud, tiktok_ud, snap_ud = _build_user_data(
        phone_e164=phone_e164,
        external_id=external_id,
        client_ip=client_ip,
        user_agent=user_agent,
        fbp=fbp,
        fbc=fbc,
        ttp=ttp,
        ttclid=ttclid,
        sc_click_id=sc_click_id,
        customer_name=None,
    )

    custom_data: dict[str, Any] = {"currency": currency}
    if value is not None:
        custom_data["value"] = value
    if content_ids:
        custom_data["content_ids"] = content_ids
        custom_data["content_type"] = "product"

    tt_props: dict[str, Any] = {"currency": currency}
    if value is not None:
        tt_props["value"] = float(value)
    if content_ids:
        tt_props["content_type"] = "product"
        tt_props["contents"] = [{"content_id": cid} for cid in content_ids]

    await asyncio.gather(
        _send_meta(event_name, event_id, event_time, event_src, meta_ud, custom_data, db),
        _send_tiktok(event_name, event_id, event_time, event_src, tiktok_ud, tt_props, db),
        _send_snap(event_name, event_id, event_time, event_src, snap_ud, custom_data, db),
        return_exceptions=True,
    )

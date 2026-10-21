from __future__ import annotations
from datetime import datetime, timezone
from fastapi import Request
from app.models.models import Order
from app.schemas.schemas import OrderIn
from app.core.phone import PhoneResult


def get_client_ip(request: Request) -> str:
    xff = request.headers.get("X-Forwarded-For")
    if xff:
        return xff.split(",")[0].strip()
    return request.client.host if request.client else ""


def build_sheet_payload(
    order: Order,
    body: OrderIn,
    phone: PhoneResult,
    client_ip: str,
    user_agent: str,
) -> dict:
    """Build the JSON payload sent to the Google Sheet webhook."""
    items_str = " | ".join(
        f"{l.slug} × {l.quantity}" + (" (upsell 99)" if l.pricing == "upsell" else "")
        for l in body.lines
    )
    # Phone local: 0 + 9 digits
    national = phone.e164[4:]  # strip +966
    phone_local = "0" + national

    # created_at as Riyadh time (UTC+3)
    from datetime import timedelta
    riyadh_offset = timezone(timedelta(hours=3))
    now = datetime.now(riyadh_offset)

    return {
        "secret": "",  # injected by sheets service from settings
        "order_id": order.public_id,
        "created_at_riyadh": now.strftime("%Y-%m-%d %H:%M"),
        "status": "new",
        "customer_name": order.customer_name,
        "phone_e164": order.phone_e164,
        "phone_local": phone_local,
        "items": items_str,
        "main_units": order.main_units,
        "upsell_accepted": "yes" if order.upsell_slug else "no",
        "upsell_slug": order.upsell_slug or "",
        "total_sar": order.total_sar,
        "currency": "SAR",
        "payment_method": "COD",
        "page_url": order.page_url or "",
        "event_id": body.event_id,
        "fbp": order.fbp or "",
        "fbc": order.fbc or "",
        "ttclid": order.ttclid or "",
        "ttp": order.ttp or "",
        "sc_click_id": order.sc_click_id or "",
        "client_ip": client_ip,
        "user_agent": user_agent,
    }

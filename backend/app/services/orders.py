from __future__ import annotations
import ipaddress
from datetime import datetime, timezone
from fastapi import Request
from app.models.models import Order
from app.schemas.schemas import OrderIn
from app.core.phone import PhoneResult


def _parsed_ip(value: str) -> ipaddress.IPv4Address | ipaddress.IPv6Address | None:
    try:
        return ipaddress.ip_address(value.strip())
    except ValueError:
        return None


def _is_global_ip(value: str) -> bool:
    addr = _parsed_ip(value)
    return bool(addr and addr.is_global)


def _is_trusted_proxy(value: str) -> bool:
    """The platform proxy is on the private Docker network, not the public internet."""
    addr = _parsed_ip(value)
    return bool(addr and not addr.is_global)


def get_client_ip(request: Request) -> str:
    """
    Visitor address for checkout.

    Forwarding headers are ignored unless the TCP peer is a trusted proxy.
    A client cannot supply a Saudi address in the first X-Forwarded-For hop
    and have it treated as the visitor. Behind Cloudflare and Easypanel the
    peer is the private proxy, and CF-Connecting-IP is the visitor address
    Cloudflare set. Otherwise the rightmost public hop is used.
    """
    peer = request.client.host if request.client else ""
    if not _is_trusted_proxy(peer):
        return peer

    cloudflare_ip = (request.headers.get("cf-connecting-ip") or "").strip()
    if _is_global_ip(cloudflare_ip):
        return cloudflare_ip

    forwarded = request.headers.get("x-forwarded-for") or ""
    for candidate in reversed([part.strip() for part in forwarded.split(",") if part.strip()]):
        if _is_global_ip(candidate):
            return candidate
    return ""


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

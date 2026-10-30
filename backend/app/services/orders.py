from __future__ import annotations
import ipaddress
from datetime import datetime, timedelta, timezone
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
        f"{l.slug} × {l.quantity}" + (f" ({l.variant})" if l.variant else "")
        for l in body.lines
    )
    # +212 is four characters, same width as the previous country code.
    national = phone.e164[4:]
    phone_local = "0" + national

    now = datetime.now(timezone(timedelta(hours=1)))
    stamp = now.strftime("%Y-%m-%d %H:%M")

    return {
        "secret": "",  # injected by sheets service from settings
        "order_id": order.public_id,
        # Existing sheet column. The value is now Africa/Casablanca local time.
        "created_at_riyadh": stamp,
        "created_at_casablanca": stamp,
        "status": "new",
        "customer_name": order.customer_name,
        "phone_e164": order.phone_e164,
        "phone_local": phone_local,
        "items": items_str,
        "main_units": order.main_units,
        "upsell_accepted": "no",
        "upsell_slug": "",
        # Existing sheet column name. The amount is MAD; currency says MAD.
        "total_sar": order.total_mad,
        "total_mad": order.total_mad,
        "shipping_mad": order.shipping_mad,
        "currency": "MAD",
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
        "city": order.city or "",
        "district": "",
        "address": order.address or "",
        "landmark": order.delivery_notes or "",
    }

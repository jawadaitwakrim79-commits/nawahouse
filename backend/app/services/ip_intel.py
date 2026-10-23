"""
IP intelligence — country geolocation + VPN/proxy detection.

Two layers, each optional:

  1. MaxMind GeoIP2 (country, city)
     - Preferred: local MMDB file (set MAXMIND_DB_PATH).
     - Fallback: MaxMind Web Services (set MAXMIND_ACCOUNT_ID + MAXMIND_LICENSE_KEY).

  2. VPN / proxy detection (choose ONE provider via VPN_PROVIDER env):
     - "ipqualityscore"  → https://ipqualityscore.com/
     - "proxycheck"      → https://proxycheck.io/
     - "ipinfo"          → https://ipinfo.io/ (requires 'Standard' plan for VPN flag)

If neither layer is configured, every request returns a conservative default:
`country_code=None`, `is_vpn=False`, `is_valid_ksa=False`. The dashboard will
then show "0 valid clicks" until credentials are added, so the operator knows
intelligence is missing — rather than silently assuming all traffic is KSA.
"""
from __future__ import annotations

import logging
import os
from dataclasses import dataclass
from typing import Optional

import httpx

from app.core.config import settings

logger = logging.getLogger(__name__)


@dataclass
class IpIntel:
    country_code: Optional[str]
    is_vpn: bool
    source: str  # e.g. "maxmind-mmdb+ipqualityscore"
    risk_score: Optional[int]  # 0..100 when available
    is_valid_ksa: bool  # country_code == "SA" AND not is_vpn

    @classmethod
    def unknown(cls, source: str = "none") -> "IpIntel":
        return cls(
            country_code=None,
            is_vpn=False,
            source=source,
            risk_score=None,
            is_valid_ksa=False,
        )


# ───────────────────────── MaxMind readers (lazy) ────────────────────────────

_mmdb_reader = None
_mmdb_tried = False


def _get_mmdb_reader():
    """Return a maxminddb Reader for the local DB, or None if unavailable."""
    global _mmdb_reader, _mmdb_tried
    if _mmdb_tried:
        return _mmdb_reader
    _mmdb_tried = True

    path = maxmind_db_path()
    if not os.path.exists(path):
        logger.warning("MaxMind MMDB not found at %s", path)
        return None
    try:
        import maxminddb  # type: ignore

        _mmdb_reader = maxminddb.open_database(path)
        logger.info("MaxMind MMDB loaded from %s", path)
    except Exception as e:  # pragma: no cover
        logger.warning("Failed to open MaxMind MMDB at %s: %s", path, e)
        _mmdb_reader = None
    return _mmdb_reader


async def _lookup_maxmind_mmdb(ip: str) -> Optional[str]:
    reader = _get_mmdb_reader()
    if reader is None:
        return None
    try:
        rec = reader.get(ip)
        if not rec:
            return None
        country = (rec.get("country") or {}).get("iso_code")
        return country
    except Exception as e:  # pragma: no cover
        logger.warning("MaxMind MMDB lookup failed for %s: %s", ip, e)
        return None


async def _lookup_maxmind_ws(ip: str) -> Optional[str]:
    """MaxMind GeoIP2 Precision Web Service fallback (paid)."""
    if not (settings.MAXMIND_ACCOUNT_ID and settings.MAXMIND_LICENSE_KEY):
        return None
    url = f"https://geoip.maxmind.com/geoip/v2.1/country/{ip}"
    try:
        async with httpx.AsyncClient(timeout=5.0) as c:
            r = await c.get(
                url,
                auth=(settings.MAXMIND_ACCOUNT_ID, settings.MAXMIND_LICENSE_KEY),
                headers={"Accept": "application/json"},
            )
        if r.status_code == 200:
            return (r.json().get("country") or {}).get("iso_code")
    except Exception as e:  # pragma: no cover
        logger.warning("MaxMind WS lookup failed for %s: %s", ip, e)
    return None


# ───────────────────────── VPN providers ─────────────────────────────────────


async def _vpn_ipqualityscore(ip: str) -> tuple[Optional[bool], Optional[int]]:
    key = settings.VPN_API_KEY
    if not key:
        return (None, None)
    url = f"https://ipqualityscore.com/api/json/ip/{key}/{ip}"
    try:
        async with httpx.AsyncClient(timeout=5.0) as c:
            r = await c.get(url, params={"strictness": 1, "allow_public_access_points": "true"})
        if r.status_code == 200:
            d = r.json()
            is_vpn = bool(d.get("vpn") or d.get("proxy") or d.get("tor") or d.get("active_vpn"))
            score = int(d.get("fraud_score") or 0)
            return (is_vpn, score)
    except Exception as e:  # pragma: no cover
        logger.warning("IPQualityScore lookup failed for %s: %s", ip, e)
    return (None, None)


async def _vpn_proxycheck(ip: str) -> tuple[Optional[bool], Optional[int]]:
    key = settings.VPN_API_KEY
    url = f"https://proxycheck.io/v2/{ip}"
    params = {"vpn": 1, "risk": 1}
    if key:
        params["key"] = key
    try:
        async with httpx.AsyncClient(timeout=5.0) as c:
            r = await c.get(url, params=params)
        if r.status_code == 200:
            d = r.json()
            node = d.get(ip, {})
            is_vpn = (node.get("proxy") == "yes") or (node.get("type") in {"VPN", "TOR"})
            risk = node.get("risk")
            score = int(risk) if isinstance(risk, (int, str)) and str(risk).isdigit() else None
            return (is_vpn, score)
    except Exception as e:  # pragma: no cover
        logger.warning("ProxyCheck lookup failed for %s: %s", ip, e)
    return (None, None)


async def _vpn_ipinfo(ip: str) -> tuple[Optional[bool], Optional[int]]:
    key = settings.VPN_API_KEY
    if not key:
        return (None, None)
    url = f"https://ipinfo.io/{ip}/privacy"
    try:
        async with httpx.AsyncClient(timeout=5.0) as c:
            r = await c.get(url, params={"token": key})
        if r.status_code == 200:
            d = r.json()
            is_vpn = bool(d.get("vpn") or d.get("proxy") or d.get("tor") or d.get("hosting"))
            return (is_vpn, None)
    except Exception as e:  # pragma: no cover
        logger.warning("IPinfo lookup failed for %s: %s", ip, e)
    return (None, None)


async def _detect_vpn(ip: str) -> tuple[Optional[bool], Optional[int], str]:
    provider = (settings.VPN_PROVIDER or "").lower().strip()
    if provider == "ipqualityscore":
        is_vpn, score = await _vpn_ipqualityscore(ip)
    elif provider == "proxycheck":
        is_vpn, score = await _vpn_proxycheck(ip)
    elif provider == "ipinfo":
        is_vpn, score = await _vpn_ipinfo(ip)
    else:
        return (None, None, "")
    return (is_vpn, score, provider)


# ───────────────────────── Public API ────────────────────────────────────────


def _is_private_ip(ip: str) -> bool:
    """Skip RFC1918 / localhost / IPv6 loopback — these are dev/local, not real traffic."""
    if not ip:
        return True
    import ipaddress

    try:
        a = ipaddress.ip_address(ip)
        return a.is_private or a.is_loopback or a.is_reserved or a.is_link_local
    except ValueError:
        return True


def maxmind_db_path() -> str:
    """Container path used when MAXMIND_DB_PATH is unset or blank."""
    path = (settings.MAXMIND_DB_PATH or "").strip()
    return path or "/app/data/GeoLite2-Country.mmdb"


def describe_maxmind() -> str:
    """One-line status for startup logs. Never includes credentials."""
    path = maxmind_db_path()
    exists = os.path.exists(path)
    loaded = _get_mmdb_reader() is not None
    return f"path={path} exists={exists} loaded={loaded}"


def checkout_block_reason(ip: str, intel: IpIntel) -> Optional[str]:
    """
    Why this IP must not place an order, or None when checkout is allowed.

    Private addresses are allowed so local development still works.
    A public IP is refused when the country is not Saudi Arabia, when a
    configured VPN check flags it, or when MaxMind could not be opened.
    An IP missing from an opened database is allowed: GeoLite2 has gaps,
    and those gaps must not stop a Saudi customer.
    """
    if not settings.STRICT_KSA_ONLY:
        return None
    if _is_private_ip(ip):
        return None
    if intel.country_code == "SA" and not intel.is_vpn:
        return None
    if intel.is_vpn:
        return "vpn"
    if intel.country_code and intel.country_code != "SA":
        return "outside_ksa"
    if "maxmind-mmdb" in intel.source or "maxmind-ws" in intel.source:
        return None
    return "geo_unavailable"


async def lookup(ip: str) -> IpIntel:
    """
    Resolve an IP → (country_code, is_vpn, is_valid_ksa).

    Returns IpIntel.unknown() when:
      - IP is private/loopback (local dev traffic)
      - No geolocation provider is configured
    A missing or unreadable MMDB is logged and returns unknown.
    It never raises, so a bad database file cannot stop the process.
    """
    if _is_private_ip(ip):
        return IpIntel.unknown(source="private")

    # 1) Country via MaxMind (prefer local MMDB, then Web Services)
    reader = _get_mmdb_reader()
    country: Optional[str] = None
    geo_source = ""
    if reader is not None:
        country = await _lookup_maxmind_mmdb(ip)
        # The database opened, even when this particular IP has no row.
        geo_source = "maxmind-mmdb"
    else:
        country = await _lookup_maxmind_ws(ip)
        geo_source = "maxmind-ws" if country else "maxmind-unavailable"

    # 2) VPN / proxy. None means the provider is not configured.
    is_vpn, risk, vpn_source = await _detect_vpn(ip)
    if is_vpn is None:
        is_vpn = False

    sources = "+".join(s for s in [geo_source, vpn_source] if s) or "none"
    valid = (country == "SA") and (not is_vpn)

    return IpIntel(
        country_code=country,
        is_vpn=is_vpn,
        source=sources,
        risk_score=risk,
        is_valid_ksa=valid,
    )

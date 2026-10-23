"""MaxMind country lookup and checkout geo gate. No live database."""
from pathlib import Path

import pytest

import app.services.ip_intel as ip_intel
from app.services.ip_intel import IpIntel


MMDB = Path(__file__).resolve().parents[1] / "data" / "GeoLite2-Country.mmdb"


def _reset_reader() -> None:
    ip_intel._mmdb_reader = None
    ip_intel._mmdb_tried = False


def test_outside_ksa_is_blocked():
    intel = IpIntel("US", False, "maxmind-mmdb", None, False)
    assert ip_intel.checkout_block_reason("8.8.8.8", intel) == "outside_ksa"


def test_saudi_ip_is_allowed():
    intel = IpIntel("SA", False, "maxmind-mmdb", None, True)
    assert ip_intel.checkout_block_reason("2.89.1.1", intel) is None


def test_private_or_unknown_country_is_rejected():
    intel = IpIntel.unknown(source="private")
    assert ip_intel.checkout_block_reason("127.0.0.1", intel) == "geo_unavailable"
    missing = IpIntel(None, False, "maxmind-mmdb", None, False)
    assert ip_intel.checkout_block_reason("8.8.8.8", missing) == "geo_unavailable"


def test_missing_maxmind_blocks_public_ip():
    intel = IpIntel.unknown(source="maxmind-unavailable")
    assert ip_intel.checkout_block_reason("8.8.8.8", intel) == "geo_unavailable"


def test_blank_path_uses_container_location(monkeypatch):
    monkeypatch.setattr(ip_intel.settings, "MAXMIND_DB_PATH", "  ")
    assert ip_intel.maxmind_db_path() == "/app/data/GeoLite2-Country.mmdb"


def test_missing_configured_path_falls_back_when_baked_file_exists(monkeypatch, tmp_path):
    baked = tmp_path / "GeoLite2-Country.mmdb"
    baked.write_bytes(b"not-opened")
    monkeypatch.setattr(ip_intel.settings, "MAXMIND_DB_PATH", str(tmp_path / "missing.mmdb"))
    monkeypatch.setattr(ip_intel, "_BAKED_MAXMIND_PATH", str(baked))
    assert ip_intel.maxmind_db_path() == str(baked)


@pytest.mark.asyncio
async def test_real_database_blocks_us_and_allows_sa(monkeypatch):
    if not MMDB.is_file():
        pytest.skip("GeoLite2-Country.mmdb is not in backend/data")
    monkeypatch.setattr(ip_intel.settings, "MAXMIND_DB_PATH", str(MMDB))
    monkeypatch.setattr(ip_intel.settings, "STRICT_KSA_ONLY", True)
    monkeypatch.setattr(ip_intel.settings, "VPN_PROVIDER", "")
    _reset_reader()

    us = await ip_intel.lookup("8.8.8.8")
    sa = await ip_intel.lookup("2.89.1.1")

    assert us.country_code == "US"
    assert us.source == "maxmind-mmdb"
    assert ip_intel.checkout_block_reason("8.8.8.8", us) == "outside_ksa"
    assert sa.country_code == "SA"
    assert ip_intel.checkout_block_reason("2.89.1.1", sa) is None
    _reset_reader()

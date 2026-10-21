"""Tests for SHA-256 hashing — verified vectors from docs/11-TRACKING-PIXELS-CAPI.md."""
import pytest
from app.core.hashing import sha256, maybe_hash


def test_meta_snap_phone():
    # Meta/Snap: hash digits without plus
    assert sha256("966512345678") == "211163de39c35e6ec1aeaa615e51b1bd275f48576ac0899d30898cef4abd5d1b"


def test_tiktok_phone():
    # TikTok: hash E.164 with plus
    assert sha256("+966512345678") == "983174e91bb83244a50493aa8e1c60ac3e44e70f64af2f2ae1798cc07b7f0c14"


def test_country_sa():
    assert sha256("sa") == "4cf6829aa93728e8f3c97df913fb1bfa95fe5810e2933a05943f8312a98d9cf2"


def test_empty_raises():
    with pytest.raises(ValueError):
        sha256("")


def test_already_hashed_passthrough():
    digest = "211163de39c35e6ec1aeaa615e51b1bd275f48576ac0899d30898cef4abd5d1b"
    assert sha256(digest) == digest  # no double-hash


def test_maybe_hash_none():
    assert maybe_hash(None) is None


def test_maybe_hash_empty():
    assert maybe_hash("") is None


def test_maybe_hash_value():
    result = maybe_hash("sa")
    assert result == "4cf6829aa93728e8f3c97df913fb1bfa95fe5810e2933a05943f8312a98d9cf2"

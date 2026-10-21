"""Tests for Saudi phone normalization."""
import pytest
from app.core.phone import normalize_sa_phone, PhoneError


# All valid inputs → +966512345678
VALID_INPUTS = [
    "0512345678",
    "512345678",
    "966512345678",
    "+966512345678",
    "00966512345678",
    "05 1234 5678",   # spaces stripped
    "05-1234-5678",   # dashes stripped
]


@pytest.mark.parametrize("inp", VALID_INPUTS)
def test_valid_mobile(inp):
    result = normalize_sa_phone(inp)
    assert result.e164 == "+966512345678"
    assert result.meta_digits == "966512345678"
    assert result.tiktok_e164 == "+966512345678"


def test_landline_rejected():
    with pytest.raises(PhoneError):
        normalize_sa_phone("0112345678")  # starts with 1, not 5


def test_too_short():
    with pytest.raises(PhoneError):
        normalize_sa_phone("12345")


def test_empty():
    with pytest.raises(PhoneError):
        normalize_sa_phone("")

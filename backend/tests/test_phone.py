"""Tests for Moroccan phone normalization."""
import pytest
from app.core.phone import normalize_ma_phone, PhoneError


VALID_INPUTS = [
    ("0612345678", "+212612345678"),
    ("612345678", "+212612345678"),
    ("212612345678", "+212612345678"),
    ("+212612345678", "+212612345678"),
    ("00212612345678", "+212612345678"),
    ("06 12 34 56 78", "+212612345678"),
    ("06-12-34-56-78", "+212612345678"),
    ("0712345678", "+212712345678"),
    ("+212 7 12 34 56 78", "+212712345678"),
    ("0512345678", "+212512345678"),
]


@pytest.mark.parametrize("raw,expected", VALID_INPUTS)
def test_valid_moroccan_number(raw, expected):
    result = normalize_ma_phone(raw)
    assert result.e164 == expected
    assert result.meta_digits == expected[1:]
    assert result.tiktok_e164 == expected


def test_saudi_number_rejected():
    with pytest.raises(PhoneError):
        normalize_ma_phone("+966512345678")


def test_too_short():
    with pytest.raises(PhoneError):
        normalize_ma_phone("12345")


def test_empty():
    with pytest.raises(PhoneError):
        normalize_ma_phone("")

"""
Phone normalisation for Nawa House / Morocco.

Accepted inputs (all map to +212 followed by 9 digits):
  06XXXXXXXX, 07XXXXXXXX, 05XXXXXXXX
  6XXXXXXXX, 7XXXXXXXX, 5XXXXXXXX
  2126XXXXXXXX, +2126XXXXXXXX, 002126XXXXXXXX

The national number is 9 digits and starts with 5, 6, or 7
(mobile 06/07, and 05 ranges used in Morocco).

Rejected:
  Saudi +966 numbers
  landline-length mistakes, short input, empty input
"""

from __future__ import annotations
import re
from dataclasses import dataclass


_ARABIC_DIGITS = str.maketrans("٠١٢٣٤٥٦٧٨٩۰۱۲۳۴۵۶۷۸۹", "01234567890123456789")
_NATIONAL_RE = re.compile(r"^[5-7]\d{8}$")


@dataclass(frozen=True)
class PhoneResult:
    e164: str
    meta_digits: str
    tiktok_e164: str


class PhoneError(ValueError):
    pass


def normalize_ma_phone(raw: str) -> PhoneResult:
    """
    Normalize a raw Moroccan phone input.
    Raises PhoneError for invalid numbers.
    """
    cleaned = (raw or "").translate(_ARABIC_DIGITS)
    cleaned = re.sub(r"[\s\-().]+", "", cleaned)

    if cleaned.startswith("+"):
        cleaned = cleaned[1:]
    if cleaned.startswith("00"):
        cleaned = cleaned[2:]

    if cleaned.startswith("212"):
        national = cleaned[3:]
    elif cleaned.startswith("0"):
        national = cleaned[1:]
    else:
        national = cleaned

    if not _NATIONAL_RE.match(national):
        raise PhoneError(
            f"Invalid Moroccan phone number: {raw!r}. "
            "Expected a Moroccan number such as 06XXXXXXXX or +2126XXXXXXXX."
        )

    digits_with_cc = "212" + national
    e164 = "+" + digits_with_cc
    return PhoneResult(e164=e164, meta_digits=digits_with_cc, tiktok_e164=e164)

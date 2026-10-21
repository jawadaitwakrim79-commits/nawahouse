"""
Phone normalisation for نوا للبيت / Nawa House.

Accepted inputs (all map to +9665XXXXXXXX):
  05XXXXXXXX
  5XXXXXXXX
  9665XXXXXXXX
  +9665XXXXXXXX
  009665XXXXXXXX

Rejected:
  0112345678   (landline — does not start with 5 after country code)
  anything that is not a Saudi mobile

Returns a PhoneResult namedtuple with:
  e164       : "+966512345678"
  meta_digits: "966512345678"   (no plus — for Meta and Snap CAPI hash)
  tiktok_e164: "+966512345678"  (with plus — for TikTok CAPI hash)
"""

from __future__ import annotations
import re
from dataclasses import dataclass


# After stripping the country code, a valid Saudi mobile is 05XXXXXXXX
# → national number = 5 followed by exactly 8 digits.
_NATIONAL_RE = re.compile(r"^5\d{8}$")


@dataclass(frozen=True)
class PhoneResult:
    e164: str         # "+966512345678"
    meta_digits: str  # "966512345678"
    tiktok_e164: str  # "+966512345678"


class PhoneError(ValueError):
    pass


def normalize_sa_phone(raw: str) -> PhoneResult:
    """
    Normalize a raw Saudi phone input.
    Raises PhoneError for invalid or non-mobile numbers.
    """
    cleaned = re.sub(r"[\s\-()]+", "", raw)

    # Strip leading +, 00
    if cleaned.startswith("+"):
        cleaned = cleaned[1:]
    if cleaned.startswith("00"):
        cleaned = cleaned[2:]

    # Accept 966XXXXXXXXX  or  05XXXXXXXX  or  5XXXXXXXX
    if cleaned.startswith("966"):
        national = cleaned[3:]
    elif cleaned.startswith("0"):
        national = cleaned[1:]
    else:
        national = cleaned

    if not _NATIONAL_RE.match(national):
        raise PhoneError(
            f"Invalid Saudi mobile number: {raw!r}. "
            "Expected format 05XXXXXXXX where X is a digit (9 digits after 0)."
        )

    digits_with_cc = "966" + national      # no plus
    e164 = "+" + digits_with_cc

    return PhoneResult(e164=e164, meta_digits=digits_with_cc, tiktok_e164=e164)

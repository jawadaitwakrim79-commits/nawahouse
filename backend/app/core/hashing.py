"""
SHA-256 hashing helpers for CAPI payloads.

Rules:
- Hash only non-empty strings.
- Do not hash a value that already looks like a 64-char hex digest.
- UTF-8, lowercase hex output.

Phone normalization before hashing:
  Meta / Snap: digits only, no plus  →  "966512345678"
  TikTok     : E.164 with plus       →  "+966512345678"
"""

from __future__ import annotations
import hashlib
import re

_ALREADY_HASHED = re.compile(r"^[0-9a-f]{64}$")


def sha256(value: str) -> str:
    """Hash a non-empty string; raises ValueError if empty or already hashed."""
    if not value:
        raise ValueError("Cannot hash an empty string")
    if _ALREADY_HASHED.match(value):
        return value  # pass-through to avoid double-hashing
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def maybe_hash(value: str | None) -> str | None:
    """Hash value if present, else return None."""
    if not value:
        return None
    return sha256(value)

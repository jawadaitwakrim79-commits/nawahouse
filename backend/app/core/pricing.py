"""
Pricing functions — the only price authority on the server.

main_total(units) → SAR
  1 → 199
  2 → 279
  3 → 349
  4 → 548 (349 + 199)
  n → 349 + 199 * (n - 3)

order_total(main_units, upsell_units) → SAR
  upsell_units must be 0 or 1
  upsell adds 99 SAR
"""

from __future__ import annotations


def main_total(units: int) -> int:
    if units <= 0:
        return 0
    if units == 1:
        return 199
    if units == 2:
        return 279
    if units == 3:
        return 349
    return 349 + 199 * (units - 3)


def order_total(main_units: int, upsell_units: int) -> int:
    if upsell_units not in (0, 1):
        raise ValueError("upsell_units must be 0 or 1")
    return main_total(main_units) + 99 * upsell_units

"""
Pricing — server authority.

Goods total is the sum of catalog prices. Shipping is added by the caller
from store settings. The client total is never trusted.
"""

from __future__ import annotations

from app.core.catalog import get_product


def goods_total(lines: list[tuple[str, int]]) -> int:
    total = 0
    for slug, quantity in lines:
        product = get_product(slug)
        if product is None:
            raise ValueError(f"Unknown product: {slug}")
        if quantity < 1:
            raise ValueError("quantity must be at least 1")
        total += product.price_mad * quantity
    return total


def order_total(goods: int, shipping_mad: int) -> int:
    if goods < 0 or shipping_mad < 0:
        raise ValueError("amounts must be zero or positive")
    return goods + shipping_mad

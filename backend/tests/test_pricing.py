"""Catalog pricing. Shipping is added by the order route, not here."""
import pytest
from app.core.pricing import goods_total, order_total


def test_single_watch():
    assert goods_total([("atlas", 1)]) == 1490


def test_two_different_products():
    assert goods_total([("lune", 1), ("dune", 1)]) == 1290 + 690


def test_quantity():
    assert goods_total([("cadre", 2)]) == 1180


def test_unknown_slug():
    with pytest.raises(ValueError):
        goods_total([("oud", 1)])


def test_order_total_adds_shipping():
    assert order_total(1490, 35) == 1525


def test_order_total_zero_shipping():
    assert order_total(540, 0) == 540


def test_negative_shipping_rejected():
    with pytest.raises(ValueError):
        order_total(540, -1)

"""Tests for pricing functions."""
import pytest
from app.core.pricing import main_total, order_total


def test_main_total_zero():
    assert main_total(0) == 0


def test_main_total_one():
    assert main_total(1) == 199


def test_main_total_two():
    assert main_total(2) == 279


def test_main_total_three():
    assert main_total(3) == 349


def test_main_total_four():
    # 349 + 199
    assert main_total(4) == 548


def test_main_total_five():
    # 349 + 199 * 2
    assert main_total(5) == 747


def test_order_total_no_upsell():
    assert order_total(2, 0) == 279


def test_order_total_with_upsell():
    assert order_total(2, 1) == 279 + 99  # 378


def test_order_total_three_with_upsell():
    assert order_total(3, 1) == 349 + 99  # 448


def test_order_total_bad_upsell():
    with pytest.raises(ValueError):
        order_total(2, 2)

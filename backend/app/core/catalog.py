"""
Product catalog — the price authority for orders.

Amounts are Moroccan dirhams. Shipping is not included here;
it is read from store settings.
"""

from __future__ import annotations
from dataclasses import dataclass


@dataclass(frozen=True)
class CatalogProduct:
    slug: str
    name_ar: str
    full_name_ar: str
    category: str
    price_mad: int
    summary: str


@dataclass(frozen=True)
class CatalogCategory:
    slug: str
    name_ar: str
    sort_order: int


CATEGORIES: tuple[CatalogCategory, ...] = (
    CatalogCategory("mens-watches", "ساعات رجالية", 1),
    CatalogCategory("womens-watches", "ساعات نسائية", 2),
    CatalogCategory("sunglasses", "نظارات شمسية", 3),
    CatalogCategory("optical", "إطارات طبية", 4),
)

PRODUCTS: dict[str, CatalogProduct] = {
    "atlas": CatalogProduct(
        "atlas", "أطلس", "ساعة أطلس الرجالية", "mens-watches", 1490,
        "ساعة كلاسيكية بعلبة فولاذية وسوار جلد.",
    ),
    "noir": CatalogProduct(
        "noir", "نوار", "ساعة نوار الرجالية", "mens-watches", 1890,
        "ساعة أوتوماتيك بسوار فولاذي وميناء أسود.",
    ),
    "lune": CatalogProduct(
        "lune", "لون", "ساعة لون النسائية", "womens-watches", 1290,
        "ساعة سهرة بميناء شامبانيا وسوار جلد.",
    ),
    "perle": CatalogProduct(
        "perle", "بيرل", "ساعة بيرل النسائية", "womens-watches", 990,
        "ساعة رفيعة بسوار شبكي معدني.",
    ),
    "dune": CatalogProduct(
        "dune", "دون", "نظارة دون الشمسية", "sunglasses", 690,
        "نظارة شمسية مستطيلة بعدسات UV400.",
    ),
    "soleil": CatalogProduct(
        "soleil", "سولاي", "نظارة سولاي الشمسية", "sunglasses", 720,
        "نظارة شمسية بعين القطة وإطار أسيتات.",
    ),
    "cadre": CatalogProduct(
        "cadre", "كادر", "إطار كادر الطبي", "optical", 590,
        "إطار طبي مستطيل من الأسيتات.",
    ),
    "ligne": CatalogProduct(
        "ligne", "لين", "إطار لين الطبي", "optical", 540,
        "إطار طبي دائري من المعدن.",
    ),
}

VALID_SLUGS = frozenset(PRODUCTS)


def get_product(slug: str) -> CatalogProduct | None:
    return PRODUCTS.get(slug)


def product_name(slug: str) -> str:
    product = PRODUCTS.get(slug)
    return product.full_name_ar if product else slug


def category_name(slug: str) -> str:
    for category in CATEGORIES:
        if category.slug == slug:
            return category.name_ar
    return slug

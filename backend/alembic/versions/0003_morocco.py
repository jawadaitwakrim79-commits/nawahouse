"""Moroccan checkout fields, MAD totals, catalog, and shipping settings.

Revision ID: 0003_morocco
Revises: 0002_page_clicks
Create Date: 2026-10-30 00:00:00

Existing order rows are kept. total_sar is renamed to total_mad so the
stored integers stay attached to the same orders. New address columns
are nullable, so older Saudi orders remain readable.
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "0003_morocco"
down_revision: Union[str, None] = "0002_page_clicks"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column("orders", "total_sar", new_column_name="total_mad")
    op.add_column(
        "orders",
        sa.Column("shipping_mad", sa.Integer(), nullable=False, server_default="0"),
    )
    op.add_column("orders", sa.Column("city", sa.Text(), nullable=True))
    op.add_column("orders", sa.Column("address", sa.Text(), nullable=True))
    op.add_column("orders", sa.Column("delivery_notes", sa.Text(), nullable=True))
    op.add_column("order_items", sa.Column("variant", sa.Text(), nullable=True))

    op.add_column(
        "products",
        sa.Column("price_mad", sa.Integer(), nullable=False, server_default="0"),
    )
    op.add_column("products", sa.Column("category", sa.Text(), nullable=True))
    op.add_column(
        "products",
        sa.Column("active", sa.Boolean(), nullable=False, server_default=sa.true()),
    )
    op.execute("UPDATE products SET price_mad = price_sar WHERE price_mad = 0")
    op.execute(
        "UPDATE products SET active = FALSE WHERE slug IN ('oud', 'shafaq', 'safa')"
    )

    op.create_table(
        "store_settings",
        sa.Column("key", sa.Text(), primary_key=True),
        sa.Column("value", sa.Text(), nullable=False),
    )
    op.execute(
        "INSERT INTO store_settings (key, value) VALUES ('shipping_mad', '0') "
        "ON CONFLICT (key) DO NOTHING"
    )

    op.create_table(
        "categories",
        sa.Column("slug", sa.Text(), primary_key=True),
        sa.Column("name_ar", sa.Text(), nullable=False),
        sa.Column("sort_order", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("active", sa.Boolean(), nullable=False, server_default=sa.true()),
    )
    op.execute(
        """
        INSERT INTO categories (slug, name_ar, sort_order, active) VALUES
        ('mens-watches', 'ساعات رجالية', 1, TRUE),
        ('womens-watches', 'ساعات نسائية', 2, TRUE),
        ('sunglasses', 'نظارات شمسية', 3, TRUE),
        ('optical', 'إطارات طبية', 4, TRUE)
        ON CONFLICT (slug) DO NOTHING
        """
    )
    op.execute(
        """
        INSERT INTO products
            (slug, name_ar, full_name_ar, enemy_ar, price_sar, price_mad, category, active)
        VALUES
        ('atlas',  'أطلس',  'ساعة أطلس الرجالية',  'ساعة كلاسيكية بعلبة فولاذية', 1490, 1490, 'mens-watches', TRUE),
        ('noir',   'نوار',  'ساعة نوار الرجالية',   'ساعة أوتوماتيك بسوار فولاذي', 1890, 1890, 'mens-watches', TRUE),
        ('lune',   'لون',   'ساعة لون النسائية',    'ساعة سهرة بميناء شامبانيا', 1290, 1290, 'womens-watches', TRUE),
        ('perle',  'بيرل',  'ساعة بيرل النسائية',   'ساعة رفيعة بسوار شبكي',     990,  990,  'womens-watches', TRUE),
        ('dune',   'دون',   'نظارة دون الشمسية',    'نظارة مستطيلة UV400',       690,  690,  'sunglasses', TRUE),
        ('soleil', 'سولاي', 'نظارة سولاي الشمسية',  'نظارة عين القطة',           720,  720,  'sunglasses', TRUE),
        ('cadre',  'كادر',  'إطار كادر الطبي',      'إطار أسيتات مستطيل',        590,  590,  'optical', TRUE),
        ('ligne',  'لين',   'إطار لين الطبي',       'إطار معدني دائري',          540,  540,  'optical', TRUE)
        ON CONFLICT (slug) DO NOTHING
        """
    )


def downgrade() -> None:
    op.execute(
        "DELETE FROM products WHERE slug IN "
        "('atlas','noir','lune','perle','dune','soleil','cadre','ligne')"
    )
    op.drop_table("categories")
    op.drop_table("store_settings")
    op.drop_column("products", "active")
    op.drop_column("products", "category")
    op.drop_column("products", "price_mad")
    op.drop_column("order_items", "variant")
    op.drop_column("orders", "delivery_notes")
    op.drop_column("orders", "address")
    op.drop_column("orders", "city")
    op.drop_column("orders", "shipping_mad")
    op.alter_column("orders", "total_mad", new_column_name="total_sar")

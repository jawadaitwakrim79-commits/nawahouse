"""initial schema and seed

Revision ID: 0001_initial
Revises:
Create Date: 2026-09-30 00:00:00

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = "0001_initial"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Sequence for public_id
    op.execute("CREATE SEQUENCE IF NOT EXISTS order_public_seq START WITH 1001")

    op.create_table(
        "products",
        sa.Column("slug", sa.Text, primary_key=True),
        sa.Column("name_ar", sa.Text, nullable=False),
        sa.Column("full_name_ar", sa.Text, nullable=False),
        sa.Column("enemy_ar", sa.Text, nullable=False),
        sa.Column("price_sar", sa.Integer, nullable=False, default=199),
    )

    op.create_table(
        "orders",
        sa.Column("id", sa.BigInteger, primary_key=True, autoincrement=True),
        sa.Column("public_id", sa.Text, unique=True, nullable=False),
        sa.Column("client_event_id", sa.Text, unique=True, nullable=False),
        sa.Column("customer_name", sa.Text, nullable=False),
        sa.Column("phone_e164", sa.Text, nullable=False),
        sa.Column("main_units", sa.Integer, nullable=False),
        sa.Column("upsell_slug", sa.Text, nullable=True),
        sa.Column("total_sar", sa.Integer, nullable=False),
        sa.Column("status", sa.Text, nullable=False, default="new"),
        sa.Column("sheet_status", sa.Text, nullable=False, default="pending"),
        sa.Column("page_url", sa.Text, nullable=True),
        sa.Column("client_ip", sa.Text, nullable=True),
        sa.Column("user_agent", sa.Text, nullable=True),
        sa.Column("fbp", sa.Text, nullable=True),
        sa.Column("fbc", sa.Text, nullable=True),
        sa.Column("ttp", sa.Text, nullable=True),
        sa.Column("ttclid", sa.Text, nullable=True),
        sa.Column("sc_click_id", sa.Text, nullable=True),
        sa.Column("external_id", sa.Text, nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("NOW()"),
            nullable=False,
        ),
    )

    op.create_index(
        "orders_phone_created_idx", "orders", ["phone_e164", "created_at"]
    )

    op.create_table(
        "order_items",
        sa.Column("id", sa.BigInteger, primary_key=True, autoincrement=True),
        sa.Column("order_id", sa.BigInteger, sa.ForeignKey("orders.id"), nullable=False),
        sa.Column("slug", sa.Text, nullable=False),
        sa.Column("quantity", sa.Integer, nullable=False),
        sa.Column("pricing", sa.Text, nullable=False),
    )

    op.create_table(
        "tracking_events",
        sa.Column("id", sa.BigInteger, primary_key=True, autoincrement=True),
        sa.Column("event_id", sa.Text, nullable=False),
        sa.Column("event_name", sa.Text, nullable=False),
        sa.Column("platform", sa.Text, nullable=False),
        sa.Column("http_status", sa.Integer, nullable=True),
        sa.Column("ok", sa.Boolean, nullable=False, default=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("NOW()"),
            nullable=False,
        ),
        sa.UniqueConstraint("event_id", "event_name", "platform", name="uq_tracking_event"),
    )

    op.create_table(
        "contact_messages",
        sa.Column("id", sa.BigInteger, primary_key=True, autoincrement=True),
        sa.Column("name", sa.Text, nullable=False),
        sa.Column("phone_e164", sa.Text, nullable=False),
        sa.Column("message", sa.Text, nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("NOW()"),
            nullable=False,
        ),
    )

    # Seed products
    op.execute(
        """
        INSERT INTO products (slug, name_ar, full_name_ar, enemy_ar, price_sar) VALUES
        ('oud',    'نوا عود',   'مبخرة عود كمبودي ذكية',      'رائحة البيت الباهتة',          199),
        ('shafaq', 'نوا شفق',   'بروجكتر شفق سينمائي',         'جو الغرفة الممل',              199),
        ('safa',   'نوا صفاء',  'منقّي هواء HEPA-13 بالعطر',  'غبار الرياض وكتمة البيت',      199)
        ON CONFLICT (slug) DO NOTHING
        """
    )


def downgrade() -> None:
    op.drop_table("contact_messages")
    op.drop_table("tracking_events")
    op.drop_table("order_items")
    op.drop_index("orders_phone_created_idx", table_name="orders")
    op.drop_table("orders")
    op.drop_table("products")
    op.execute("DROP SEQUENCE IF EXISTS order_public_seq")

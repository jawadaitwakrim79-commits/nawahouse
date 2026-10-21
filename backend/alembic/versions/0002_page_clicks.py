"""add page_clicks table for admin dashboard

Revision ID: 0002_page_clicks
Revises: 0001_initial
Create Date: 2026-10-15 00:00:00

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = "0002_page_clicks"
down_revision: Union[str, None] = "0001_initial"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "page_clicks",
        sa.Column("id", sa.BigInteger, primary_key=True, autoincrement=True),
        sa.Column("session_id", sa.Text, nullable=False),
        sa.Column("path", sa.Text, nullable=False),
        sa.Column("referrer", sa.Text, nullable=True),
        sa.Column("utm_source", sa.Text, nullable=True),
        sa.Column("utm_medium", sa.Text, nullable=True),
        sa.Column("utm_campaign", sa.Text, nullable=True),
        sa.Column("fbclid", sa.Text, nullable=True),
        sa.Column("ttclid", sa.Text, nullable=True),
        sa.Column("sc_click_id", sa.Text, nullable=True),
        sa.Column("client_ip", sa.Text, nullable=True),
        sa.Column("user_agent", sa.Text, nullable=True),
        sa.Column("country_code", sa.Text, nullable=True),
        sa.Column("is_vpn", sa.Boolean, nullable=False, server_default=sa.text("false")),
        sa.Column("is_valid_ksa", sa.Boolean, nullable=False, server_default=sa.text("false")),
        sa.Column("intel_source", sa.Text, nullable=True),
        sa.Column("risk_score", sa.Integer, nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("NOW()"),
            nullable=False,
        ),
    )
    op.create_index("page_clicks_session_idx", "page_clicks", ["session_id"])
    op.create_index("page_clicks_ip_idx", "page_clicks", ["client_ip"])
    op.create_index("page_clicks_country_idx", "page_clicks", ["country_code"])
    op.create_index("page_clicks_valid_ksa_idx", "page_clicks", ["is_valid_ksa"])
    op.create_index("page_clicks_created_idx", "page_clicks", ["created_at"])


def downgrade() -> None:
    op.drop_index("page_clicks_created_idx", table_name="page_clicks")
    op.drop_index("page_clicks_valid_ksa_idx", table_name="page_clicks")
    op.drop_index("page_clicks_country_idx", table_name="page_clicks")
    op.drop_index("page_clicks_ip_idx", table_name="page_clicks")
    op.drop_index("page_clicks_session_idx", table_name="page_clicks")
    op.drop_table("page_clicks")

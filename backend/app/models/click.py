from __future__ import annotations
from datetime import datetime
from sqlalchemy import BigInteger, Boolean, DateTime, Integer, Text, func
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base


class PageClick(Base):
    """
    One row per page view / landing event from the public site.
    Only rows with `is_valid_ksa = TRUE` are counted in dashboard metrics
    (unless the admin explicitly views the "all traffic" filter).

    `is_valid_ksa` is set by IpIntelService at insert time:
    - True  → country_code == "SA" AND is_vpn is False
    - False → anything else (foreign IP, VPN/proxy, datacenter)
    """

    __tablename__ = "page_clicks"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)

    # Session / request
    session_id: Mapped[str] = mapped_column(Text, nullable=False, index=True)
    path: Mapped[str] = mapped_column(Text, nullable=False)
    referrer: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Attribution (ad network query params)
    utm_source: Mapped[str | None] = mapped_column(Text, nullable=True)
    utm_medium: Mapped[str | None] = mapped_column(Text, nullable=True)
    utm_campaign: Mapped[str | None] = mapped_column(Text, nullable=True)
    fbclid: Mapped[str | None] = mapped_column(Text, nullable=True)
    ttclid: Mapped[str | None] = mapped_column(Text, nullable=True)
    sc_click_id: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Request fingerprint
    client_ip: Mapped[str | None] = mapped_column(Text, nullable=True, index=True)
    user_agent: Mapped[str | None] = mapped_column(Text, nullable=True)

    # IP intelligence (populated by IpIntelService)
    country_code: Mapped[str | None] = mapped_column(Text, nullable=True, index=True)
    is_vpn: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    is_valid_ksa: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=False, index=True
    )
    intel_source: Mapped[str | None] = mapped_column(Text, nullable=True)
    # risk_score: 0 (safe) → 100 (certain fraud). Null when provider unavailable.
    risk_score: Mapped[int | None] = mapped_column(Integer, nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False, index=True
    )

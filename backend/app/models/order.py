from datetime import datetime
from typing import Optional
from sqlalchemy import BigInteger, Integer, Text, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base


class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    public_id: Mapped[str] = mapped_column(Text, unique=True, nullable=False)
    client_event_id: Mapped[str] = mapped_column(Text, unique=True, nullable=False)
    customer_name: Mapped[str] = mapped_column(Text, nullable=False)
    phone_e164: Mapped[str] = mapped_column(Text, nullable=False)
    main_units: Mapped[int] = mapped_column(Integer, nullable=False)
    upsell_slug: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    total_sar: Mapped[int] = mapped_column(Integer, nullable=False)
    status: Mapped[str] = mapped_column(Text, nullable=False, default="new")
    sheet_status: Mapped[str] = mapped_column(Text, nullable=False, default="skipped")
    page_url: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    client_ip: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    user_agent: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    fbp: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    fbc: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    ttp: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    ttclid: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    sc_click_id: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    external_id: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=datetime.utcnow
    )

    items: Mapped[list["OrderItem"]] = relationship(
        "OrderItem", back_populates="order", cascade="all, delete-orphan"
    )


class OrderItem(Base):
    __tablename__ = "order_items"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    order_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("orders.id"), nullable=False)
    slug: Mapped[str] = mapped_column(Text, nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    pricing: Mapped[str] = mapped_column(Text, nullable=False)  # 'main' or 'upsell'

    order: Mapped["Order"] = relationship("Order", back_populates="items")

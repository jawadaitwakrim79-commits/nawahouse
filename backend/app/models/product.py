from sqlalchemy import Integer, Text
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base


class Product(Base):
    __tablename__ = "products"

    slug: Mapped[str] = mapped_column(Text, primary_key=True)
    name_ar: Mapped[str] = mapped_column(Text, nullable=False)
    full_name_ar: Mapped[str] = mapped_column(Text, nullable=False)
    enemy_ar: Mapped[str] = mapped_column(Text, nullable=False)
    price_sar: Mapped[int] = mapped_column(Integer, nullable=False, default=199)

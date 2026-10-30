from __future__ import annotations
from typing import Literal
from pydantic import BaseModel, field_validator, model_validator
import re

from app.core.catalog import VALID_SLUGS


class OrderLineIn(BaseModel):
    slug: str
    quantity: int
    pricing: Literal["main", "upsell"] = "main"
    variant: str | None = None

    @field_validator("slug")
    @classmethod
    def validate_slug(cls, v: str) -> str:
        if v not in VALID_SLUGS:
            raise ValueError(f"slug must be one of {sorted(VALID_SLUGS)}")
        return v

    @field_validator("quantity")
    @classmethod
    def validate_quantity(cls, v: int) -> int:
        if not (1 <= v <= 6):
            raise ValueError("quantity must be 1–6")
        return v

    @field_validator("variant")
    @classmethod
    def validate_variant(cls, v: str | None) -> str | None:
        if v is None:
            return None
        v = v.strip()
        if not v:
            return None
        if len(v) > 40:
            raise ValueError("variant is too long")
        return v


class OrderIn(BaseModel):
    event_id: str
    name: str
    phone: str
    city: str
    address: str
    delivery_notes: str | None = None
    lines: list[OrderLineIn]
    page_url: str | None = None
    fbp: str | None = None
    fbc: str | None = None
    ttp: str | None = None
    ttclid: str | None = None
    sc_click_id: str | None = None
    external_id: str | None = None
    event_source_url: str | None = None

    @field_validator("event_id")
    @classmethod
    def validate_uuid(cls, v: str) -> str:
        _UUID_RE = re.compile(
            r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$",
            re.IGNORECASE,
        )
        if not _UUID_RE.match(v):
            raise ValueError("event_id must be a UUID")
        return v

    @field_validator("name")
    @classmethod
    def validate_name(cls, v: str) -> str:
        v = v.strip()
        if len(v) < 2 or len(v) > 60:
            raise ValueError("name must be 2–60 characters")
        if re.fullmatch(r"[\d\s]+", v):
            raise ValueError("name must not be digits only")
        return v

    @field_validator("city")
    @classmethod
    def validate_city(cls, v: str) -> str:
        v = v.strip()
        if len(v) < 2 or len(v) > 60:
            raise ValueError("city must be 2–60 characters")
        return v

    @field_validator("address")
    @classmethod
    def validate_address(cls, v: str) -> str:
        v = v.strip()
        if len(v) < 4 or len(v) > 200:
            raise ValueError("address must be 4–200 characters")
        return v

    @field_validator("delivery_notes")
    @classmethod
    def validate_notes(cls, v: str | None) -> str | None:
        if v is None:
            return None
        v = v.strip()
        if not v:
            return None
        if len(v) > 300:
            raise ValueError("delivery notes must be 300 characters or fewer")
        return v

    @model_validator(mode="after")
    def validate_lines(self) -> "OrderIn":
        if not self.lines:
            raise ValueError("at least one line is required")
        if any(line.pricing != "main" for line in self.lines):
            raise ValueError("only main lines are accepted")
        return self


class OrderOut(BaseModel):
    order_id: str
    event_id: str
    total_mad: int
    shipping_mad: int = 0
    currency: str = "MAD"


class EventIn(BaseModel):
    event_name: str
    event_id: str
    page_url: str | None = None
    value: float | None = None
    currency: str | None = "MAD"
    content_ids: list[str] | None = None
    phone: str | None = None
    external_id: str | None = None
    fbp: str | None = None
    fbc: str | None = None
    ttp: str | None = None
    ttclid: str | None = None
    sc_click_id: str | None = None


FORBIDDEN_PURCHASE_EVENTS = {"Purchase", "CompletePayment", "PURCHASE"}


class ContactIn(BaseModel):
    name: str
    phone: str
    message: str

    @field_validator("name")
    @classmethod
    def validate_name(cls, v: str) -> str:
        v = v.strip()
        if len(v) < 2:
            raise ValueError("name too short")
        return v

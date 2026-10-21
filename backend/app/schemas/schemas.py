from __future__ import annotations
from typing import Literal
from pydantic import BaseModel, field_validator, model_validator
import re


VALID_SLUGS = {"oud", "shafaq", "safa"}


class OrderLineIn(BaseModel):
    slug: str
    quantity: int
    pricing: Literal["main", "upsell"]

    @field_validator("slug")
    @classmethod
    def validate_slug(cls, v: str) -> str:
        if v not in VALID_SLUGS:
            raise ValueError(f"slug must be one of {VALID_SLUGS}")
        return v

    @field_validator("quantity")
    @classmethod
    def validate_quantity(cls, v: int) -> int:
        if not (1 <= v <= 6):
            raise ValueError("quantity must be 1–6")
        return v


class OrderIn(BaseModel):
    event_id: str
    name: str
    phone: str
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

    @model_validator(mode="after")
    def validate_lines(self) -> "OrderIn":
        main_lines = [l for l in self.lines if l.pricing == "main"]
        upsell_lines = [l for l in self.lines if l.pricing == "upsell"]
        if not main_lines:
            raise ValueError("at least one main line is required")
        if len(upsell_lines) > 1:
            raise ValueError("at most one upsell line")
        if upsell_lines and upsell_lines[0].quantity != 1:
            raise ValueError("upsell quantity must be 1")
        return self


class OrderOut(BaseModel):
    order_id: str
    event_id: str
    total_sar: int
    currency: str = "SAR"


class EventIn(BaseModel):
    event_name: str
    event_id: str
    page_url: str | None = None
    value: float | None = None
    currency: str | None = "SAR"
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

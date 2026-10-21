from typing import Optional, Literal
from pydantic import BaseModel, UUID4, field_validator
import re


VALID_SLUGS = {"oud", "shafaq", "safa"}


class OrderLine(BaseModel):
    slug: str
    quantity: int
    pricing: Literal["main", "upsell"]

    @field_validator("slug")
    @classmethod
    def validate_slug(cls, v: str) -> str:
        if v not in VALID_SLUGS:
            raise ValueError(f"Invalid slug: {v!r}")
        return v

    @field_validator("quantity")
    @classmethod
    def validate_quantity(cls, v: int) -> int:
        if not 1 <= v <= 6:
            raise ValueError("Quantity must be between 1 and 6")
        return v


class OrderCreate(BaseModel):
    event_id: str
    name: str
    phone: str
    lines: list[OrderLine]
    client_total: Optional[int] = None  # Optional; server validates and rejects if it differs
    page_url: Optional[str] = None
    fbp: Optional[str] = None
    fbc: Optional[str] = None
    ttp: Optional[str] = None
    ttclid: Optional[str] = None
    sc_click_id: Optional[str] = None
    external_id: Optional[str] = None
    event_source_url: Optional[str] = None

    @field_validator("name")
    @classmethod
    def validate_name(cls, v: str) -> str:
        v = v.strip()
        if len(v) < 2 or len(v) > 60:
            raise ValueError("Name must be 2-60 characters")
        if re.match(r"^\d+$", v):
            raise ValueError("Name must not be digits only")
        return v


class OrderResponse(BaseModel):
    order_id: str
    event_id: str
    total_sar: int
    currency: str = "SAR"


class EventPayload(BaseModel):
    event_name: str
    event_id: str
    page_url: Optional[str] = None
    value: Optional[float] = None
    currency: str = "SAR"
    content_ids: Optional[list[str]] = None
    phone: Optional[str] = None
    fbp: Optional[str] = None
    fbc: Optional[str] = None
    ttp: Optional[str] = None
    ttclid: Optional[str] = None
    sc_click_id: Optional[str] = None
    external_id: Optional[str] = None
    user_agent: Optional[str] = None
    client_ip: Optional[str] = None
    contents: Optional[list[dict]] = None


BLOCKED_EVENT_NAMES = {"Purchase", "CompletePayment", "PURCHASE"}


class ContactCreate(BaseModel):
    name: str
    phone: str
    message: str

    @field_validator("name")
    @classmethod
    def validate_name(cls, v: str) -> str:
        v = v.strip()
        if len(v) < 2 or len(v) > 60:
            raise ValueError("Name must be 2-60 characters")
        return v

    @field_validator("message")
    @classmethod
    def validate_message(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("Message is required")
        return v

from __future__ import annotations

from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.models.models import ContactMessage
from app.schemas.schemas import ContactIn
from app.core.phone import normalize_sa_phone, PhoneError
from fastapi import HTTPException

router = APIRouter()


@router.post("/contact", status_code=201)
async def contact(
    body: ContactIn,
    request: Request,
    db: AsyncSession = Depends(get_db),
) -> dict:
    try:
        phone = normalize_sa_phone(body.phone)
    except PhoneError as exc:
        raise HTTPException(status_code=422, detail=str(exc))

    msg = ContactMessage(
        name=body.name.strip(),
        phone_e164=phone.e164,
        message=body.message.strip(),
    )
    db.add(msg)
    await db.commit()
    return {"ok": True}

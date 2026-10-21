from __future__ import annotations
import logging
import httpx
from app.core.config import settings

logger = logging.getLogger(__name__)


async def send_to_sheet(payload: dict) -> bool:
    url = settings.SHEET_WEBHOOK_URL
    if not url:
        logger.info("SHEET_WEBHOOK_URL not set — skipping sheet")
        return False

    # Inject secret into payload
    payload = {**payload, "secret": settings.SHEET_WEBHOOK_SECRET}

    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            r = await client.post(url, json=payload)
            if r.status_code == 200:
                data = r.json()
                return data.get("ok", False)
            logger.warning("Sheet webhook returned %s", r.status_code)
            return False
    except Exception as exc:
        logger.error("Sheet webhook error: %s", exc)
        return False

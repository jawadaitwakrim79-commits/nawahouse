import logging

from fastapi import APIRouter
from fastapi.responses import JSONResponse

from app.db.session import ping_db, public_db_error

router = APIRouter()
logger = logging.getLogger(__name__)


@router.get("/health")
async def health():
    """Report the process as healthy only when the database answers."""
    try:
        await ping_db()
    except Exception as exc:
        logger.error("health check database query failed: %s", public_db_error(exc))
        return JSONResponse(status_code=503, content={"ok": False, "db": "down"})
    return {"ok": True, "db": "up"}

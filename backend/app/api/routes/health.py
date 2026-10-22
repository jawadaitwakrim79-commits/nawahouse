import logging

from fastapi import APIRouter
from fastapi.responses import JSONResponse

from app.db.session import ping_db, public_db_error

router = APIRouter()
logger = logging.getLogger(__name__)


@router.get("/health")
async def health():
    """
    Liveness probe.  Returns 200 as long as the Python process is alive.
    Does NOT touch the database — a transient DB hiccup must not cause
    Easypanel to kill and restart a perfectly healthy process.
    """
    return {"status": "ok"}


@router.get("/health/db")
async def health_db():
    """
    Readiness / database probe — separate from the liveness endpoint.
    Call this from monitoring scripts; do NOT use it as the Easypanel
    health-check path, because a momentary DB blip would restart the server.
    """
    try:
        await ping_db()
    except Exception as exc:
        logger.error("db health check failed: %s", public_db_error(exc))
        return JSONResponse(status_code=503, content={"status": "db_down"})
    return {"status": "ok", "db": "up"}

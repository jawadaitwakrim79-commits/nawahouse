from __future__ import annotations
import logging
import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.api.router import router
from app.admin.router import router as admin_router
from app.admin.api import router as admin_api_router
from app.db.session import database_target, ping_db, public_db_error

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def _rss_mb() -> str:
    """Peak RSS in MiB. Linux reports ru_maxrss in kilobytes; 'n/a' if unavailable."""
    try:
        import resource
        return f"{resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024:.1f}"
    except Exception:
        return "n/a"


@asynccontextmanager
async def lifespan(app: FastAPI):
    # NOTE: we deliberately do NOT install custom signal handlers here.
    # Uvicorn registers SIGTERM / SIGINT through asyncio's event loop
    # (loop.add_signal_handler).  Replacing those handlers with synchronous
    # signal.signal() calls breaks Uvicorn's graceful-drain logic.
    # The lifespan finally-block is sufficient for shutdown diagnostics.
    logger.info(
        "startup pid=%s database=%s rss_mb=%s",
        os.getpid(),
        database_target(),
        _rss_mb(),
    )
    try:
        await ping_db()
    except Exception as exc:
        logger.error("startup database connection failed: %s", public_db_error(exc))
        raise RuntimeError("database connection failed during startup") from None
    logger.info("startup database connection ok")
    try:
        yield
    finally:
        logger.info("shutdown rss_mb=%s", _rss_mb())


app = FastAPI(title="Nawa House API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
    allow_credentials=False,
)

app.include_router(router)
app.include_router(admin_router)
app.include_router(admin_api_router)

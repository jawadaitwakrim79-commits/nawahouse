from __future__ import annotations
import logging
import os
import signal
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.api.router import router
from app.admin.router import router as admin_router
from app.db.session import database_target, ping_db, public_db_error

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

_PREVIOUS_SIGNALS: dict[int, signal.Handlers] = {}


def _rss_mb() -> str:
    """Peak RSS in MiB. Linux reports ru_maxrss in kilobytes. 'n/a' if unsupported."""
    try:
        import resource

        return f"{resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024:.1f}"
    except Exception:
        return "n/a"


def _install_shutdown_logging() -> None:
    """Log SIGTERM/SIGINT, then keep uvicorn's own handler so shutdown still happens."""

    def handler(signum: int, frame) -> None:
        try:
            name = signal.Signals(signum).name
        except ValueError:
            name = str(signum)
        logger.warning(
            "received %s rss_mb=%s; the process was asked to stop by the outside, not by an application exception",
            name,
            _rss_mb(),
        )
        previous = _PREVIOUS_SIGNALS.get(signum)
        if previous not in (None, signal.SIG_DFL, signal.SIG_IGN) and callable(previous):
            previous(signum, frame)

    for sig in (signal.SIGTERM, signal.SIGINT):
        try:
            _PREVIOUS_SIGNALS[sig] = signal.signal(sig, handler)
        except (ValueError, OSError) as exc:
            logger.info("could not install handler for signal %s: %s", sig, type(exc).__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    _install_shutdown_logging()
    logger.info(
        "startup pid=%s database=%s rss_mb=%s maxmind=disabled",
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
        logger.info("shutdown complete rss_mb=%s", _rss_mb())


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

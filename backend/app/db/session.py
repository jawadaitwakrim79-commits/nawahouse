from __future__ import annotations
import re
from collections.abc import AsyncGenerator
from urllib.parse import urlparse

from sqlalchemy import text
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from app.core.config import settings

engine = create_async_engine(
    settings.ASYNC_DATABASE_URL,
    echo=False,
    pool_pre_ping=True,
    connect_args={"ssl": False} if "nawahouse_database" in settings.DATABASE_URL else {},
)

AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)


def database_target() -> str:
    """Host and port only. The password and username are never included."""
    parsed = urlparse(settings.ASYNC_DATABASE_URL)
    host = parsed.hostname or "unknown"
    port = parsed.port or 5432
    return f"{host}:{port}"


def public_db_error(exc: BaseException) -> str:
    """Exception text with any database URL removed."""
    message = re.sub(r"postgres(?:ql)?(?:\+\w+)?://\S+", "postgresql://***", str(exc))
    return f"{type(exc).__name__}: {message}"


async def ping_db() -> None:
    """Open a connection and run SELECT 1. Raises if the database is unreachable."""
    async with engine.connect() as conn:
        await conn.execute(text("SELECT 1"))


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session

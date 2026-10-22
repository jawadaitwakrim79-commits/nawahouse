"""Health endpoint and startup diagnostics — no live database required."""
import pytest

from app.api.routes.health import health, health_db
from app.core.config import _normalize_db_url
from app.db.session import public_db_error


def test_database_url_strips_sslmode_and_uses_asyncpg():
    url = _normalize_db_url(
        "postgres://nawahouse:nawahouse@nawahouse_database:5432/nawahouse?sslmode=disable"
    )
    assert url == "postgresql+asyncpg://nawahouse:nawahouse@nawahouse_database:5432/nawahouse"


def test_public_db_error_hides_url():
    exc = ConnectionError("failed postgresql://nawahouse:secret@nawahouse_database:5432/nawahouse")
    text = public_db_error(exc)
    assert "secret" not in text
    assert "postgresql://***" in text
    assert text.startswith("ConnectionError:")


@pytest.mark.asyncio
async def test_health_returns_200_without_any_db_call():
    """
    /health must not touch the database.
    It must return {"status": "ok"} regardless of whether the DB is reachable —
    because Easypanel uses this endpoint to decide whether to restart the container.
    """
    result = await health()
    assert result == {"status": "ok"}


@pytest.mark.asyncio
async def test_health_does_not_call_ping_db(monkeypatch):
    """Verify that /health never calls ping_db even if we monkey-patch it to fail."""
    async def should_not_be_called():
        raise AssertionError("/health must not call ping_db")

    monkeypatch.setattr("app.api.routes.health.ping_db", should_not_be_called)
    result = await health()
    assert result == {"status": "ok"}


@pytest.mark.asyncio
async def test_health_db_is_up_when_database_answers(monkeypatch):
    async def ok():
        return None

    monkeypatch.setattr("app.api.routes.health.ping_db", ok)
    result = await health_db()
    assert result == {"status": "ok", "db": "up"}


@pytest.mark.asyncio
async def test_health_db_is_down_when_database_raises(monkeypatch):
    async def fail():
        raise ConnectionError("postgresql://user:secret@db/nawahouse")

    monkeypatch.setattr("app.api.routes.health.ping_db", fail)
    response = await health_db()
    assert response.status_code == 503
    body = response.body
    assert b"secret" not in body
    assert b"db_down" in body

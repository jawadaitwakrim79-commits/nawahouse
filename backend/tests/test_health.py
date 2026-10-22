"""Health reporting and shutdown diagnostics. No live database."""
import signal

import pytest

from app.api.routes.health import health
from app.core.config import _normalize_db_url
from app.db.session import public_db_error
from app.main import _install_shutdown_logging, _PREVIOUS_SIGNALS


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
async def test_health_is_up_only_when_database_answers(monkeypatch):
    async def ok():
        return None

    monkeypatch.setattr("app.api.routes.health.ping_db", ok)
    assert await health() == {"ok": True, "db": "up"}


@pytest.mark.asyncio
async def test_health_is_down_when_database_raises(monkeypatch):
    async def fail():
        raise ConnectionError("postgresql://user:secret@db/nawahouse")

    monkeypatch.setattr("app.api.routes.health.ping_db", fail)
    response = await health()
    assert response.status_code == 503
    assert b'"db":"down"' in response.body or b'"db": "down"' in response.body
    assert b"secret" not in response.body


def test_shutdown_handler_logs_and_calls_previous():
    seen = []

    def previous(signum, frame):
        seen.append(signum)

    old_term = signal.signal(signal.SIGTERM, signal.SIG_DFL)
    old_int = signal.signal(signal.SIGINT, signal.SIG_DFL)
    try:
        signal.signal(signal.SIGTERM, previous)
        _install_shutdown_logging()
        handler = signal.getsignal(signal.SIGTERM)
        handler(signal.SIGTERM, None)
        assert seen == [signal.SIGTERM]
    finally:
        signal.signal(signal.SIGTERM, old_term)
        signal.signal(signal.SIGINT, old_int)
        _PREVIOUS_SIGNALS.clear()

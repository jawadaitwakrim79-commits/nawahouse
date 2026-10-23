"""Admin login and dashboard API. Queries are stubbed; no live database."""
import pytest
from fastapi.testclient import TestClient

from app.admin.queries import Metrics
from app.core.config import settings
from app.db.session import get_db
from app.main import app


async def _no_db():
    yield None


@pytest.fixture
def client(monkeypatch):
    async def ping():
        return None

    monkeypatch.setattr("app.main.ping_db", ping)
    monkeypatch.setattr(settings, "ADMIN_TOKEN", "")
    monkeypatch.setattr(settings, "ADMIN_USERNAME", "")
    monkeypatch.setattr(settings, "ADMIN_PASSWORD", "")
    app.dependency_overrides[get_db] = _no_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


def test_admin_pages_are_not_missing(client):
    page = client.get("/admin")
    overview = client.get("/api/admin/overview")
    assert page.status_code != 404
    assert overview.status_code != 404
    assert page.status_code == 503
    assert overview.status_code == 503


def test_login_is_disabled_until_configured(client):
    response = client.post("/api/admin/login", json={"token": "anything"})
    assert response.status_code == 503


def test_login_rejects_wrong_token(client, monkeypatch):
    monkeypatch.setattr(settings, "ADMIN_TOKEN", "correct-token")
    response = client.post("/api/admin/login", json={"token": "wrong-token"})
    assert response.status_code == 401


def test_login_session_reads_live_query_results(client, monkeypatch):
    monkeypatch.setattr(settings, "ADMIN_TOKEN", "correct-token")
    login = client.post("/api/admin/login", json={"token": "correct-token"})
    assert login.status_code == 200
    session = login.json()["session"]
    assert session != "correct-token"
    assert "correct-token" not in session

    async def metrics(db, date_from, date_to, include_invalid=False):
        return Metrics(
            date_from=date_from,
            date_to=date_to,
            total_clicks=4,
            valid_ksa_clicks=2,
            vpn_clicks=1,
            foreign_clicks=1,
            unique_sessions=3,
            orders_count=1,
            orders_revenue=199,
            conversion_rate=0.5,
        )

    async def series(db, date_from, date_to):
        return [{"date": "2026-10-01", "clicks": 2, "orders": 1}]

    async def products(db, date_from, date_to):
        return [{"slug": "oud", "qty": 1}]

    async def orders(db, date_from, date_to, status_filter=None, limit=100, offset=0):
        return []

    monkeypatch.setattr("app.admin.api.compute_metrics", metrics)
    monkeypatch.setattr("app.admin.api.daily_series", series)
    monkeypatch.setattr("app.admin.api.top_products", products)
    monkeypatch.setattr("app.admin.api.list_orders", orders)

    denied = client.get("/api/admin/overview")
    assert denied.status_code == 401

    allowed = client.get("/api/admin/overview", headers={"Authorization": f"Bearer {session}"})
    assert allowed.status_code == 200
    body = allowed.json()
    assert body["orders_count"] == 1
    assert body["orders_revenue"] == 199
    assert body["conversion_rate"] == 0.5
    assert body["orders"] == []

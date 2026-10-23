"""Checkout country gate. Lookups and the database are mocked."""
import pytest
from fastapi.testclient import TestClient
from starlette.requests import Request

from app.db.session import get_db
from app.main import app
from app.services.ip_intel import IpIntel
from app.services.orders import get_client_ip


def _request(peer: str, headers: dict[str, str]) -> Request:
    scope = {
        "type": "http",
        "asgi": {"version": "3.0"},
        "http_version": "1.1",
        "method": "POST",
        "scheme": "https",
        "path": "/api/orders",
        "raw_path": b"/api/orders",
        "query_string": b"",
        "headers": [(name.lower().encode(), value.encode()) for name, value in headers.items()],
        "client": (peer, 443),
        "server": ("api.nawahouse.shop", 443),
    }
    return Request(scope)


def test_direct_peer_ignores_spoofed_saudi_forwarding_header():
    request = _request("8.8.8.8", {"X-Forwarded-For": "2.89.1.1", "CF-Connecting-IP": "2.89.1.1"})
    assert get_client_ip(request) == "8.8.8.8"


def test_trusted_proxy_uses_cloudflare_visitor_not_the_spoofed_first_hop():
    request = _request(
        "10.11.0.4",
        {"X-Forwarded-For": "2.89.1.1, 104.16.0.1", "CF-Connecting-IP": "105.154.0.8"},
    )
    assert get_client_ip(request) == "105.154.0.8"


def test_trusted_proxy_uses_the_rightmost_public_forwarded_address():
    request = _request("172.18.0.3", {"X-Forwarded-For": "2.89.1.1, 41.140.128.10"})
    assert get_client_ip(request) == "41.140.128.10"


def test_trusted_proxy_without_a_public_address_has_no_client_ip():
    request = _request("10.11.0.4", {"X-Forwarded-For": "10.0.0.5"})
    assert get_client_ip(request) == ""


class Recorder:
    def __init__(self):
        self.added = []
        self.commits = 0

    def add(self, obj):
        self.added.append(obj)

    async def scalar(self, stmt):
        sql = str(stmt).lower()
        if "nextval" in sql:
            return 1001
        if "count" in sql:
            return 0
        return None

    async def flush(self):
        return None

    async def commit(self):
        self.commits += 1

    async def refresh(self, obj):
        return None


def _order(event_id: str, phone: str = "0512345678") -> dict:
    return {
        "event_id": event_id,
        "name": "اختبار",
        "phone": phone,
        "lines": [{"slug": "oud", "quantity": 1, "pricing": "main"}],
    }


@pytest.fixture
def gate(monkeypatch):
    recorder = Recorder()
    seen = []

    async def ping():
        return None

    async def no_network(*args, **kwargs):
        return True

    async def _db():
        yield recorder

    monkeypatch.setattr("app.main.ping_db", ping)
    monkeypatch.setattr("app.api.routes.orders.send_to_sheet", no_network)
    monkeypatch.setattr("app.api.routes.orders.send_purchase_capi", no_network)

    def install(intel_for):
        async def lookup(ip: str):
            seen.append(ip)
            result = intel_for(ip)
            if isinstance(result, Exception):
                raise result
            return result

        monkeypatch.setattr("app.api.routes.orders.lookup_ip", lookup)

    app.dependency_overrides[get_db] = _db
    with TestClient(app) as client:
        yield client, recorder, seen, install
    app.dependency_overrides.clear()


def test_saudi_lookup_is_the_only_order_endpoint_that_can_save(gate):
    client, recorder, seen, install = gate
    install(lambda ip: IpIntel("SA", False, "maxmind-mmdb", None, True))
    response = client.post("/api/orders", json=_order("aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa"))
    assert response.status_code == 201
    assert len(recorder.added) == 2
    assert recorder.commits == 2
    assert client.post("/api/visits", json={}).status_code == 404
    assert client.post("/api/admin/orders", json={}).status_code in {401, 403, 404, 405, 422}


@pytest.mark.parametrize(
    ("intel", "event_id"),
    [
        (IpIntel("MA", False, "maxmind-mmdb", None, False), "bbbbbbbb-bbbb-4bbb-8bbb-bbbbbbbbbbbb"),
        (IpIntel("US", False, "maxmind-mmdb", None, False), "cccccccc-cccc-4ccc-8ccc-cccccccccccc"),
        (IpIntel.unknown("maxmind-unavailable"), "dddddddd-dddd-4ddd-8ddd-dddddddddddd"),
        (RuntimeError("mmdb"), "eeeeeeee-eeee-4eee-8eee-eeeeeeeeeeee"),
    ],
)
def test_non_saudi_and_failed_lookups_save_nothing(gate, intel, event_id):
    client, recorder, seen, install = gate
    install(lambda ip: intel)
    response = client.post(
        "/api/orders",
        json=_order(event_id),
        headers={"X-Forwarded-For": "2.89.1.1", "CF-Connecting-IP": "2.89.1.1"},
    )
    assert response.status_code == 403
    assert recorder.added == []
    assert recorder.commits == 0
    assert seen == ["testclient"]


def test_health_stays_independent_of_maxmind(gate, monkeypatch):
    client, recorder, seen, install = gate

    def explode():
        raise AssertionError("health must not open MaxMind")

    monkeypatch.setattr("app.api.routes.health._get_mmdb_reader", explode, raising=False)
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
    assert recorder.added == []

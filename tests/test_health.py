from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health() -> None:
    r = client.get("api/health")
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}


def test_uptime() -> None:
    r = client.get("api/health/uptime")
    assert r.status_code == 200
    assert r.json()["uptime_seconds"] >= 0

from http import HTTPStatus


def test_health_ok(client):
    r = client.get("/api/health")
    assert r.status_code == HTTPStatus.OK
    assert r.json()["status"] == "healthy"
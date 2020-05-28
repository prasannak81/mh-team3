import sys

print(sys.path)

from quickpickup import api


def test_index_works():
    client = api.app.test_client()
    resp = client.get("/")
    assert resp.status_code == 200
    assert "ok" in resp.get_json()


def test_mongo_version():
    client = api.app.test_client()
    resp = client.get("/mongo/version")
    assert resp.get_json() == {"version": "3.10.1"}

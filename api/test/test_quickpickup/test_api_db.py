import os
from unittest import mock

import pytest

from quickpickup import db
from quickpickup import api
from quickpickup import hooks


# This disables these tests unless `INTEGRATION_TEST` env var is non-empty
pytestmark = pytest.mark.skipif(
    os.environ.get("UNIT_ONLY", False), reason="Integration tests not run",
)


#########
# WARNING
#
# This module relies on the database being stateful for tests, reordering tests
# will break things. This isn't great, but it's quick an dirty.


def teardown_module():
    db.collection("test").delete_many({})
    db.collection("test_hook").delete_many({})
    db.collection("spots").delete_many({})


def test_create_fails_without_post_body():
    client = api.app.test_client()
    resp = client.post("/create/test/1")

    assert resp.status_code == 400


def test_create_works():
    client = api.app.test_client()
    resp = client.post("/create/test/1", json={"test": True})

    assert resp.status_code == 200
    assert resp.get_json() == {"_id": "1"}


def test_update_works():
    client = api.app.test_client()
    resp = client.put("/update/test/1", json={"updated": True})

    assert resp.status_code == 200
    assert resp.get_json() == {"_id": "1", "test": True, "updated": True}


def test_update_modifies_in_place():
    client = api.app.test_client()
    resp = client.put("/update/test/1", json={"updated": False, "test": False})

    assert resp.status_code == 200
    assert resp.get_json() == {"_id": "1", "test": False, "updated": False}


def test_read_works():
    client = api.app.test_client()
    resp = client.get("/read/test/1")

    assert resp.status_code == 200
    assert resp.get_json() == [{"_id": "1", "test": False, "updated": False}]


def test_read_gets_all():
    client = api.app.test_client()
    client.post("/create/test/2", json={"test": 2})

    resp = client.get("/read/test/")

    assert resp.status_code == 200
    assert resp.get_json() == [
        {"_id": "1", "test": False, "updated": False},
        {"_id": "2", "test": 2},
    ]


def test_read_handles_int_types():
    client = api.app.test_client()
    resp = client.get("/read/test/", query_string={"test": 2})

    assert resp.status_code == 200
    assert resp.get_json() == [
        {"_id": "2", "test": 2},
    ]


def test_read_handles_bool_types():
    client = api.app.test_client()
    resp = client.get("/read/test/", query_string={"test": "false"})

    assert resp.status_code == 200
    assert resp.get_json() == [
        {"_id": "1", "test": False, "updated": False},
    ]


def test_hooks_work():
    class TestHook:
        def create(self, _id, obj):
            obj["hooked"] = True
            return obj

        def update(self, _id, obj):
            obj["unhooked"] = True
            return obj

    hooks.register("test_hook", TestHook())

    # Chaining behavior here 'cause I'm lazy about fixutres

    client = api.app.test_client()
    resp = client.post("/create/test_hook/1", json={"test": True})
    assert resp.get_json() == {"_id": "1"}

    resp = client.get("/read/test_hook/1")
    assert resp.get_json() == [{"_id": "1", "test": True, "hooked": True}]

    resp = client.put("/update/test_hook/1", json={"updated": False, "test": False})
    assert resp.get_json() == {
        "_id": "1",
        "test": False,
        "updated": False,
        "hooked": True,
        "unhooked": True,
    }

    resp = client.get("/read/test_hook/1")
    assert resp.get_json() == [
        {"_id": "1", "test": False, "updated": False, "hooked": True, "unhooked": True}
    ]


@mock.patch("requests.post")
def test_chatbot_hook(post):
    client = api.app.test_client()
    resp = client.post("/create/spots/1", json={"test": True})
    assert resp.get_json() == {"_id": "1"}

    payload = {
        "orderNumber": "Threeve",
        "_orderready": {"customerName": "Bob Testerton"},
    }

    resp = client.put("/update/spots/1", json=payload)
    assert resp.get_json() == {
        "_id": "1",
        "test": True,
        "orderNumber": "Threeve",
    }

    post.assert_called_once()

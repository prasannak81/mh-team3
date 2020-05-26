import os

import pytest

from quickpickup import db
from quickpickup import api


# This disables these tests unless `INTEGRATION_TEST` env var is non-empty
pytestmark = pytest.mark.skipif(
    not os.environ.get("INTEGRATION_TEST", False),
    reason="Integration tests not available",
)


#########
# WARNING
#
# This module relies on the database being stateful for tests, reordering tests
# will break things. This isn't great, but it's quick an dirty.


def teardown_module():
    db.collection("test").delete_many({})


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

import os

import pytest

from quickpickup import db
from quickpickup import api


# This disables these tests unless `INTEGRATION_TEST` env var is non-empty
pytestmark = pytest.mark.skipif(
    not os.environ.get("INTEGRATION_TEST", False),
    reason="Integration tests not available",
)


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

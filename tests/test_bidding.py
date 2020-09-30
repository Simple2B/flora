import pytest

from app.models import WorkItem
from app import db, create_app
from tests.utils import register, login, logout


@pytest.fixture
def client():
    app = create_app(environment="testing")
    app.config["TESTING"] = True

    with app.test_client() as client:
        app_ctx = app.app_context()
        app_ctx.push()
        db.drop_all()
        db.create_all()
        register("sam")
        login(client, "sam")
        yield client
        db.session.remove()
        db.drop_all()
        app_ctx.pop()


def test_bidding(client):
    response = client.get("/bidding")
    assert response.status_code == 200
    assert b"Overhead" in response.data
    item = WorkItem(name="TESTWORKITEM", code="99.99")
    item.save()
    response = client.get("/bidding")
    assert b"TESTWORKITEM" in response.data
    assert b"99.99" in response.data

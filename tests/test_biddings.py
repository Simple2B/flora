import pytest

from app import db, create_app
from tests.utils import register, login
from app.controllers import populate_db_by_test_data, bid_generation


@pytest.fixture
def client():
    app = create_app(environment="testing")
    app.config["TESTING"] = True

    with app.test_client() as client:
        app_ctx = app.app_context()
        app_ctx.push()
        db.drop_all()
        db.create_all()
        bid_generation()
        populate_db_by_test_data()
        register("sam")
        login(client, "sam")
        yield client
        db.session.remove()
        db.drop_all()
        app_ctx.pop()


def test_biddings(client):
    response = client.get("/biddings")
    assert response.status_code == 200
    assert b"Client" in response.data
    test = 0

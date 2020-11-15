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
        populate_db_by_test_data()
        bid_generation()
        register("sam")
        login(client, "sam")
        yield client
        db.session.remove()
        db.drop_all()
        app_ctx.pop()


def test_edited_bids(client):
    response = client.post("/edited_bids", data={'1': 'on', '2': 'on'}, follow_redirects=True)
    assert response.status_code == 200
    assert b'Archived' in response.data


def test_biddings(client):
    response = client.get("/biddings")
    assert response.status_code == 200
    assert b"Client" in response.data

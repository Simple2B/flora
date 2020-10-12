import pytest

from app import db, create_app
from tests.utils import register, login


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
    response = client.get("/biddings", follow_redirects=True)
    assert response.status_code == 200
    assert b'103' in response.data
    # TODO: check if suitable records exist in the DB with status NEW
    # Bids.

import pytest

from app import db, create_app
from tests.utils import register, login, logout
from app.models import Bid, Alternate
from app.controllers.db_population import populate_db_by_test_data

USER_NAME = "sam"
USER_PASS = "SuperPa$$w0rd"

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
        register("sam")
        login(client, "sam")
        yield client
        db.session.remove()
        db.drop_all()
        app_ctx.pop()


def test_add_alternate(client):
    bid = Bid.query.first()
    res = client.get(f"/alternate/new/{bid.id}")
    assert res.status_code == 200
    pass

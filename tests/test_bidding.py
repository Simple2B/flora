import pytest

from app import db, create_app
from tests.utils import register, login
from app.controllers.db_population import populate_db_by_test_data
from app.models import Bid


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


def test_bidding(client):
    bids = Bid.query.all()
    for bid in bids:
        if bid.status.value == "New":
            response = client.get("/bidding/{}".format(bid.id))
            assert response.status_code == 200
            string_bid_id = str(bid.id).encode('utf-8')
            assert string_bid_id in response.data
            assert b'Add work item/group' in response.data

    # TODO: check if suitable records exist in the DB with status NEW
    # Bids.

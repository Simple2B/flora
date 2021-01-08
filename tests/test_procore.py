import pytest
from app import db, create_app
from tests.utils import register, login
from app.controllers import populate_db_by_test_data, bid_generation
from app.procore import ProcoreApi


@pytest.fixture
def client():
    app = create_app(environment="testing")
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


def _test_get_bids(client):
    papi = ProcoreApi()
    bids_from_procore = papi.bids(ignore_testing=True)
    assert bids_from_procore

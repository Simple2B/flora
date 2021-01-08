import pytest
from datetime import datetime

from app import db, create_app
from tests.utils import register, login
from app.controllers import populate_db_by_test_data, bid_generation
from app.logger import log


@pytest.fixture
def client():
    app = create_app(environment="testing")
    app.config["TESTING_PROCORE_API"] = True

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


def test_procore_api(client):
    now = datetime.now()
    response = client.get("/biddings", follow_redirects=True)
    assert response.status_code == 200
    then = datetime.now()
    seconds = (then - now).seconds
    log(log.INFO, f'All test pass in {seconds} seconds')

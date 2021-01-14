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
    ADD_URL = f"/alternate/new/{bid.id}"
    res = client.get(ADD_URL)
    assert res.status_code == 200
    ALT_NAME = "Some alternate"
    res = client.post(ADD_URL, data=dict(
        name=ALT_NAME,
        tbd=True,
        description="Some alternate description",
        quantity=56,
        unit="LS",
        price=100
    ))
    assert res.status_code == 302
    assert "bidding" in res.location
    assert "#alternates" in res.location
    # assert b'Alternate added successful.' in res.data
    bid = Bid.query.get(bid.id)
    assert bid.alternates
    assert bid.alternates[0].name == ALT_NAME

    logout(client)
    res = client.get(ADD_URL)
    assert res.status_code == 302
    assert "login" in res.location


def test_edit_alternate(client):
    bid = Bid.query.first()
    ADD_URL = f"/alternate/new/{bid.id}"
    ALT_NAME = "Some alternate"
    res = client.post(ADD_URL, data=dict(
        name=ALT_NAME,
        tbd=True,
        description="Some alternate description",
        quantity=56,
        unit="LS",
        price=100
    ))
    assert res.status_code == 302
    assert "bidding" in res.location
    bid = Bid.query.get(bid.id)
    assert bid.alternates
    alternate_id = bid.alternates[0].id
    EDIT_URL = f"/alternate/edit/{bid.id}/{alternate_id}"
    ALT_NAME_EDITED = "Some alternate (Edited)"
    res = client.post(EDIT_URL, data=dict(
        name=ALT_NAME_EDITED,
        tbd=True,
        description="Some alternate description",
        quantity=56,
        unit="LS",
        price=100
    ))
    assert res.status_code == 302
    assert "bidding" in res.location
    assert "#alternates" in res.location
    # assert b'Alternate added successful.' in res.data
    bid = Bid.query.get(bid.id)
    assert bid.alternates
    assert len(bid.alternates) == 1
    assert bid.alternates[0].name == ALT_NAME_EDITED

    logout(client)
    res = client.get(EDIT_URL)
    assert res.status_code == 302
    assert "login" in res.location


def test_delete_alternate(client):
    bid = Bid.query.first()
    ADD_URL = f"/alternate/new/{bid.id}"
    res = client.get(ADD_URL)
    assert res.status_code == 200
    ALT_NAME = "Some alternate"
    res = client.post(ADD_URL, data=dict(
        name=ALT_NAME,
        tbd=True,
        description="Some alternate description",
        quantity=56,
        unit="LS",
        price=100
    ))
    assert res.status_code == 302
    assert "bidding" in res.location
    bid = Bid.query.get(bid.id)
    assert bid.alternates
    alternate_id = bid.alternates[0].id
    DELETE_URL = f"/alternate/delete/{bid.id}/{alternate_id}"
    res = client.get(DELETE_URL)
    assert res.status_code == 302
    assert "bidding" in res.location
    assert "#alternates" in res.location
    bid = Bid.query.get(bid.id)
    assert not bid.alternates

    logout(client)
    res = client.get(ADD_URL)
    assert res.status_code == 302
    assert "login" in res.location

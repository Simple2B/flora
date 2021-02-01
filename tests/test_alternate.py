import pytest

from app import db, create_app
from tests.utils import register, login, logout
from app.models import Bid
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
    assert "#bid_alternates" in res.location
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
    EDIT_URL = f"/alternate/edit/{bid.id}/{alternate_id}"
    ALT_NAME_EDITED = "Some alternate (Edited)"
    ALT_TBD_EDITED = True
    ALT_DESCRIPTION_EDITED = "Some alternate description"
    ALT_QUANTITY_EDITED = 56
    ALT_UNIT_EDITED = "LS"
    ALT_PRICE_EDITED = 100

    res = client.post(EDIT_URL, data=dict(
        name=ALT_NAME_EDITED,
        tbd=ALT_TBD_EDITED,
        description=ALT_DESCRIPTION_EDITED,
        quantity=ALT_QUANTITY_EDITED,
        unit=ALT_UNIT_EDITED,
        price=ALT_PRICE_EDITED
    ))
    assert res.status_code == 302
    assert "bidding" in res.location
    assert "#bid_alternates" in res.location
    # assert b'Alternate added successful.' in res.data
    bid = Bid.query.get(bid.id)
    assert bid.alternates
    assert len(bid.alternates) == 1
    assert bid.alternates[0].name == ALT_NAME_EDITED
    assert bid.alternates[0].tbd == ALT_TBD_EDITED
    assert bid.alternates[0].description == ALT_DESCRIPTION_EDITED
    assert bid.alternates[0].quantity == ALT_QUANTITY_EDITED
    assert bid.alternates[0].unit == ALT_UNIT_EDITED
    assert bid.alternates[0].price == ALT_PRICE_EDITED

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
    assert "#bid_alternates" in res.location
    bid = Bid.query.get(bid.id)
    assert not bid.alternates

    logout(client)
    res = client.get(ADD_URL)
    assert res.status_code == 302
    assert "login" in res.location


# test for getting errors
def test_add_alternate_errors(client):
    bid = Bid.query.first()
    ADD_URL = f"/alternate/new/{bid.id}"
    res = client.get(ADD_URL)
    assert res.status_code == 200
    NAME = "VERY LONG STRING!!! "*10
    res = client.post(ADD_URL, data=dict(
        name=NAME,
        tbd=True,
        description="Some alternate description",
    ))
    assert res.status_code == 200
    assert b'This field is required.' in res.data or b'Field must be between 1 and 128 characters long.' in res.data


def test_edit_alternate_errors(client):
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
    assert bid.alternates
    alternate_id = bid.alternates[0].id
    EDIT_URL = f"/alternate/edit/{bid.id}/{alternate_id}"
    res = client.post(EDIT_URL, data=dict(
        tbd=True,
        description="Some alternate description",
        quantity=56,
        unit="LS",
        price=100
    ))
    assert res.status_code == 200
    assert b'This field is required.' in res.data

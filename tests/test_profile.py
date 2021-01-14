import pytest

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


def test_profile(client):
    response = client.get("/profile")
    assert response.status_code == 200
    assert b"Account Information" in response.data
    response = client.post("/profile", data=dict(
            username="sam",
            email="sam@test.com",
            position="test position",
            phone=123456789
        ))
    assert response.status_code == 302
    logout(client)
    response = client.get("/profile")
    assert response.status_code == 302
    assert "login" in response.location


def test_save_blank_fields(client):
    response = client.post("/profile", data=dict(
            username="",
            email="sam@test.com",
            position="test position",
            phone=123456789,
            password="password",
            password_confirmation="password",
        ))
    assert response.status_code == 200
    assert b'This field is required.' in response.data, "username required"

    response = client.post("/profile", data=dict(
            username="user",
            email="",
            position="test position",
            phone=123456789,
            password="password",
            password_confirmation="password",
        ))
    assert response.status_code == 200
    assert b'This field is required.' in response.data, "email required"

    response = client.post("/profile", data=dict(
            username="user",
            email="sam@test.com",
            position="",
            phone=123456789,
            password="password",
            password_confirmation="password",
        ))
    assert response.status_code == 200, "position required"
    assert b'This field is required.' in response.data, "position required"

    response = client.post("/profile", data=dict(
            username="user",
            email="sam@test.com",
            position="test position",
            phone="",
            password="password",
            password_confirmation="password",
        ))
    assert response.status_code == 200, "phone required"
    assert b'This field is required.' in response.data, "phone required"


def test_save_wrong_email_short_password(client):
    response = client.post("/profile", data=dict(
            username="user_name",
            email="sam.test.com",
            position="test position",
            phone=123456789,
            password="pass",
            password_confirmation="password",
        ))
    assert response.status_code == 200
    assert b'Invalid email address.' in response.data
    assert b'Password do not match.' in response.data
    assert b'Password field must be between 6 and 30 characters long.' in response.data

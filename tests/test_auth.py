import pytest

from app import db, create_app
from tests.utils import register, login, logout
from app.models import User


@pytest.fixture
def client():
    app = create_app(environment="testing")
    app.config["TESTING"] = True

    with app.test_client() as client:
        app_ctx = app.app_context()
        app_ctx.push()
        db.drop_all()
        db.create_all()
        yield client
        db.session.remove()
        db.drop_all()
        app_ctx.pop()


def test_auth_pages(client):
    response = client.get("/register")
    assert response.status_code == 302
    response = client.get("/login")
    assert response.status_code == 200
    response = client.get("/logout")
    assert response.status_code == 302


def test_register(client):
    response = client.post(
        "/register",
        data=dict(
            username="sam",
            email="sam@test.com",
            user_type="admin",
            position="test position",
            phone=123456789,
            password="password",
            password_confirmation="password",
        ),
        follow_redirects=True,
    )
    assert b"Registration successful. You are logged in." in response.data


def test_login_and_logout(client):
    # Access to logout view before login should fail.
    response = logout(client)
    assert b"Please log in to access this page." in response.data
    register("sam")
    response = login(client, "sam")
    assert b"sam" in response.data
    # Should successfully logout the currently logged in user.
    response = logout(client)
    assert b"You were logged out." in response.data
    # Incorrect login credentials should fail.
    response = login(client, "sam", "wrongpassword")
    assert b"Wrong user login/email or password." in response.data
    # Correct credentials should login
    response = login(client, "sam")
    assert b"sam" in response.data


def test_edit_user(client):
    register("sam")
    login(client, "sam")
    u = User.query.get(1)
    # /edit_card/<int:user_id>
    EDIT_USER_URL = "/edit_card/1"
    TEST_USER_NAME = "UserName"
    TEST_EMAIL = "user@bubu.com"
    TEST_PASS = "Pa$$word1"
    res = client.post(EDIT_USER_URL, data=dict(
        username=TEST_USER_NAME,
        email=TEST_EMAIL,
        position="Boss",
        phone="00000000",
        password=TEST_PASS,
        password_confirmation=TEST_PASS,
        user_type=u.user_type.value
    ))
    assert res.status_code == 302
    u = User.query.get(1)
    assert u.username == TEST_USER_NAME
    assert u.email == TEST_EMAIL

    res = client.post(EDIT_USER_URL, data=dict(
        username=TEST_USER_NAME,
        email=TEST_EMAIL,
        position="Boss",
        phone="00000000",
        password=TEST_PASS,
        password_confirmation="Another value"
    ), follow_redirects=True)
    assert res.status_code == 200
    assert b"Password do not match" in res.data

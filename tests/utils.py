from app.models import User


def register(
    username,
    email="sam@test.com",
    user_type="admin",
    position="test position",
    phone=123456789,
    password="password"
):
    user = User(
        username=username,
        email=email,
        user_type=user_type,
        position=position,
        phone=phone,
        password=password,
    )
    user.save()
    return user.id


def login(client, username, password="password"):
    return client.post(
        "/login", data=dict(user_id=username, password=password), follow_redirects=True
    )


def logout(client):
    return client.get("/logout", follow_redirects=True)

from app.models import User


def register(
    username,
    email="sam@test.com",
    user_type="admin",
    position="test position",
    phone=123456789,
    password="password",
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


# Test data
TEST_BIDS = [
    {'awarded': None, 'bid_package_id': 99, 'bid_package_title': 'Bidding 1',
        'name': 'Zradogog Daggozyr - f8cbc82c-517e-41c9-99de-41d5440829b6',
        'bidder_comments': None, 'company_id': 27948, 'created_at': '2020-10-09T11:10:59Z',
        'due_date': '2020-10-09T11:00:00Z', 'id': 129},
    {'awarded': None, 'bid_package_id': 102, 'bid_package_title': 'Bidding 2',
        'name': 'Subcontracting TEST Company', 'bidder_comments': None,
        'company_id': 27948, 'created_at': '2020-10-11T17:43:37Z', 'due_date': '2020-10-11T17:00:00Z', 'id': 134},
    {'awarded': None, 'bid_package_id': 103, 'bid_package_title': 'Bidding 3',
        'name': 'Subcontracting TEST Company', 'bidder_comments': None,
        'company_id': 27948, 'created_at': '2020-10-11T17:55:57Z', 'due_date': '2020-10-11T17:00:00Z', 'id': 135},
    {'awarded': None, 'bid_package_id': 104, 'bid_package_title': 'Bidding 4',
        'name': 'Architect TEST Company', 'bidder_comments': None,
        'company_id': 27948, 'created_at': '2020-10-11T17:56:54Z', 'due_date': '2020-10-11T17:00:00Z', 'id': 136}]

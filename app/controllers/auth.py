from app.models import User


def add_user_data_validator(username, email, phone):
    if User.query.filter(User.username == username).first():
        return False
    if User.query.filter(User.email == email).first():
        return False
    if User.query.filter(User.phone == phone).first():
        return False
    return True

import os
import pytest

from app import db, create_app
from app.controllers import create_docx, populate_db_by_test_data, bid_generation


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
        yield client
        db.session.remove()
        db.drop_all()
        app_ctx.pop()


def test_create_docx(client):
    filepath = create_docx(1)
    os.remove(filepath)

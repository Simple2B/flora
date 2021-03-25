import os
import pytest

from app import db, create_app
from app.models import Bid
from app.controllers import create_docx, populate_db_by_test_data


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
        client.files_to_remove = []
        yield client
        for file in client.files_to_remove:
            os.remove(file)
        db.session.remove()
        db.drop_all()
        app_ctx.pop()


def test_create_docx(client):
    BID_ID = Bid.query.first().id
    assert BID_ID
    file_path = create_docx(BID_ID)
    assert file_path
    assert os.path.isfile(file_path)
    client.files_to_remove += [file_path]

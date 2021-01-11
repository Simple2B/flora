import pytest
from app import db, create_app
from tests.utils import register, login
from app.controllers import populate_db_by_test_data, bid_generation
from app.procore import ProcoreApi


@pytest.fixture
def client():
    app = create_app(environment="testing")
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


def _test_get_bids(client):
    papi = ProcoreApi()
    for _ in range(10):
        bids_from_procore = papi.bids(ignore_testing=True)
        assert bids_from_procore


def _est_get_all_drawing(client):
    papi = ProcoreApi()
    bids = papi.bids(ignore_testing=True)
    assert bids
    projects = papi.projects
    assert projects
    for bid_no, bid in enumerate(bids):
        project = bid['project'] if 'project' in bid else None
        assert project
        project_name = project['name'] if 'name' in project else None
        assert project_name
        project_id = None
        for project in projects:
            assert 'name' in project
            if project['name'] == project_name:
                project_id = project['id']
                break
        # assert project_id
        if not project_id:
            continue

        drawing_uploads = papi.drawing_uploads(project_id)
        if not drawing_uploads:
            continue
        # assert drawing_uploads, f"for project_id:[{project_id}] on bid_no:{bid_no}"

        drawing_areas = set()
        for drawing_upload in drawing_uploads:
            assert "drawing_area_id" in drawing_upload
            drawing_areas.add(drawing_upload["drawing_area_id"])
        assert drawing_areas
        bid_drawings = []
        for drawing_area_id in drawing_areas:
            drawings = papi.drawings(drawing_area_id)
            assert drawings
            bid_drawings += drawings
        assert bid_drawings

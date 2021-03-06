import datetime

from app.procore import ProcoreApi
from app.models import Bid, Drawing
from app.logger import log
from app import db


def update_bids():
    log(log.INFO, "Read bids form ProCore")
    papi = ProcoreApi()
    projects = None
    bids_from_procore = papi.bids()
    log(log.INFO, "Got [%d] bids", len(bids_from_procore))
    # assert bids_from_procore
    need_commit = False
    for bid in bids_from_procore:
        if "id" not in bid:
            log(log.ERROR, "Wrong bid entity format")
            continue
        bid_id = bid["id"]
        db_bid = Bid.query.filter(Bid.procore_bid_id == bid_id).first()
        if not db_bid:
            log(log.INFO, "Add new bid [%s]", bid_id)
            if "project" not in bid:
                log(log.ERROR, "Bad bid format [%s]. Not found [project]", bid_id)
                continue
            if "vendor" not in bid:
                log(log.ERROR, "Bad bid format [%s]. Not found [vendor]", bid_id)
                continue
            if "bid_package_title" not in bid:
                log(
                    log.ERROR,
                    "Bad bid format [%s]. Not found [bid_package_title]",
                    bid_id,
                )
                continue
            if "address" not in bid["project"]:
                log(
                    log.ERROR,
                    "Bad bid format [%s]. Not found [project.address]",
                    bid_id,
                )
                continue

            vendor_address = bid["bid_requester"]["vendor_address"]
            v_addr_lines = vendor_address.split("<br>")
            project_address = bid["project"]["address"]
            p_addr_lines = project_address.split("<br>")
            bid_requester = bid["bid_requester"]
            contact_lines = bid_requester["contact"].split(" (")
            due_date = bid["due_date"]
            due_date = datetime.datetime.strptime(due_date, "%Y-%m-%dT%H:%M:%SZ")

            bidding = Bid(
                procore_bid_id=bid["id"],
                title=bid["bid_package_title"],
                client=(
                    bid["vendor"]["name"] if "name" in bid["vendor"] else "Unknown name"
                ),
                project_name=bid['project']['name'],
                vendor_address_street=(v_addr_lines[0] if v_addr_lines else ""),
                vendor_address_city=(v_addr_lines[1] if len(v_addr_lines) > 1 else ""),
                address_street=(p_addr_lines[0] if p_addr_lines else ""),
                address_city=(p_addr_lines[1] if len(p_addr_lines) > 1 else ""),
                phone=bid_requester["business_phone"],
                email=bid_requester["email_address"],
                fax=bid_requester["fax_number"],
                contact=(contact_lines[0] if contact_lines else ""),
                due_date=due_date,
            )
            bidding.save(commit=False)
            if not projects:
                projects = papi.projects
            add_drawings_for_bid(bid, projects, papi, bidding)
            need_commit = True

    if need_commit:
        db.session.commit()


def add_drawings_for_bid(bid, projects, papi, bidding):
    project = bid["project"] if "project" in bid else None
    if not project:
        log(log.ERROR, "bid has not attribute project")
        return
    project_name = project["name"] if "name" in project else None
    assert project_name
    if not project_name:
        log(log.ERROR, "project has not attribute name")
        return
    project_id = None
    for project in projects:
        assert "name" in project
        if project["name"] == project_name:
            project_id = project["id"]
            break
    # assert project_id
    if not project_id:
        return

    drawing_uploads = papi.drawing_uploads(project_id)
    if not drawing_uploads:
        return

    drawing_areas = set()
    for drawing_upload in drawing_uploads:
        assert "drawing_area_id" in drawing_upload
        drawing_areas.add(drawing_upload["drawing_area_id"])
    if not drawing_areas:
        return
    for drawing_area_id in drawing_areas:
        drawings = papi.drawings(drawing_area_id)
        assert drawings
        for drawing in drawings:
            if 'current_revision' in drawing:
                current_revision = drawing["current_revision"]
                if "pdf_url" not in current_revision and "png_url" not in current_revision:
                    continue
                Drawing(
                    bid=bidding,
                    number=drawing["number"] if "number" in drawing else "???",
                    title=drawing["title"] if "title" in drawing else "???",
                    revision_number=current_revision["revision_number"]
                    if "revision_number" in current_revision
                    else "???",
                    updated_at=datetime.datetime.strptime(
                        current_revision["updated_at"], "%Y-%m-%dT%H:%M:%SZ"
                    )
                    if "updated_at" in current_revision
                    else datetime.datetime.now(),
                    pdf_url=current_revision["pdf_url"] if "pdf_url" in current_revision else "",
                    png_url=current_revision["png_url"] if "png_url" in current_revision else ""
                ).save(commit=False)

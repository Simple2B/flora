import datetime

from app.procore import ProcoreApi
from app.models import Bid, Drawing
from app.logger import log
from app import db


def update_bids():
    log(log.INFO, "Read bids form ProCore")
    papi = ProcoreApi()
    projects = None
    bids_from_procore = papi.get_bids()
    log(log.INFO, "Got [%d] bids", len(bids_from_procore))
    need_commit = False
    for bid in bids_from_procore:
        if "project_id" not in bid:
            log(log.ERROR, "Wrong bid entity format")
            continue
        project_id = bid["project_id"]
        procore_id = bid["procore_id"]
        db_bid = Bid.query.filter(Bid.procore_bid_id == procore_id).first()
        if not db_bid:
            log(log.INFO, "Add new bid [%s]", procore_id)
            bidding = Bid(
                procore_bid_id=procore_id,
                title=bid["name"],
                client=bid["client"],
                vendor_address_street=bid["client_address"],
                vendor_address_city=bid["client_city"],
                address_street=bid["address_street"],
                address_city=bid["adress_city"],
                phone=bid["business_phone"],
                email=bid["email"],
                fax=bid["fax_number"],
                contact=bid["contact_name"],
                due_date=bid["due_date"],
            )
            bidding.save(commit=False)
            if not projects:
                projects = papi.projects
            add_drawings_for_bid(project_id, projects, papi, bidding)
            need_commit = True

    if need_commit:
        db.session.commit()


def add_drawings_for_bid(project_id, projects, papi, bidding):
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

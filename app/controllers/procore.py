from app.procore import ProcoreApi
from app.models import Bid
from app.logger import log
from app import db


def update_bids():
    log(log.INFO, 'Read bids form ProCore')
    papi = ProcoreApi()
    bids_from_procore = papi.bids()
    log(log.INFO, 'Got [%d] bids', len(bids_from_procore))
    # assert bids_from_procore
    need_commit = False
    for bid in bids_from_procore:
        if "id" not in bid:
            log(log.ERROR, "Wrong bid entity format")
            continue
        bid_id = bid["id"]
        db_bid = Bid.query.filter(Bid.procore_bid_id == bid_id).first()
        if not db_bid:
            log(log.INFO, 'Add new bid [%s]', bid_id)
            if "project" not in bid:
                log(log.ERROR, "Bad bid format [%s]. Not found [project]", bid_id)
                continue
            if "vendor" not in bid:
                log(log.ERROR, "Bad bid format [%s]. Not found [vendor]", bid_id)
                continue
            if "bid_package_title" not in bid:
                log(log.ERROR, "Bad bid format [%s]. Not found [bid_package_title]", bid_id)
                continue
            if "address" not in bid["project"]:
                log(log.ERROR, "Bad bid format [%s]. Not found [project.address]", bid_id)
                continue

            address = bid["project"]["address"]
            addr_lines = address.split("<br>")

            bidding = Bid(
                procore_bid_id=bid["id"],
                title=bid["bid_package_title"],
                client=(bid["vendor"]["name"] if "name" in bid["vendor"] else "Unknown name"),
                address_street=(addr_lines[0] if addr_lines else ""),
                address_city=(addr_lines[1] if len(addr_lines) > 1 else "")
            )
            bidding.save(commit=False)
            need_commit = True

    if need_commit:
        db.session.commit()

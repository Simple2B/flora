from app.procore import ProcoreApi
from app.models import Bid
from app.logger import log


def update_bids():
    log(log.INFO, 'Read bids form ProCore')
    papi = ProcoreApi()
    bids_from_procore = papi.bids()
    log(log.INFO, 'Got [%d] bids', len(bids_from_procore))
    # assert bids_from_procore
    for bid in bids_from_procore:
        bid_id = bid["id"]
        db_bid = Bid.query.filter(Bid.procore_bid_id == bid_id).first()
        if not db_bid:
            log(log.INFO, 'Add new bid [%s]', bid["id"])
            bidding = Bid(
                procore_bid_id=bid["id"],
                title=bid["bid_package_title"],
                client=bid["vendor"]["name"],
            )
            bidding.save()

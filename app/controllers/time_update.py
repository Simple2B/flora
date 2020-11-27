import time
from app.models import Bid


def time_update(bid_id):
    bid = Bid.query.get(bid_id)
    if bid:
        bid.time_updated = round(time.time())
        bid.save()

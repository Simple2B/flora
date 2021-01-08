from app import db
from app.models import Bid


def bid_generation():
    Bid(
        procore_bid_id=106,
        title="bidding 5",
        client="Procore (Test Companies)",
        status=Bid.Status.b_draft
    ).save(commit=False)

    for i in range(3):
        Bid(
            procore_bid_id=107+i,
            title="bidding i",
            client="Test company",
            status=Bid.Status.c_submitted
        ).save(commit=False)

    for i in range(4):
        Bid(
            procore_bid_id=110+i,
            title=f"bidding {3+i}",
            client="Procore (Test Companies)",
            status=Bid.Status.d_archived
        ).save(commit=False)

    db.session.commit()

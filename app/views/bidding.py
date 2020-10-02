from flask import Blueprint, render_template
from flask_login import login_required

from app.models import Bid

bidding_blueprint = Blueprint("bidding", __name__)


@bidding_blueprint.route("/biddings")
@login_required
def biddings():
    for i in range(9):
        bid_test = Bid()
        bid_test.save()
    bids = Bid.query.all()
    return render_template("biddings.html", bids=bids)


@bidding_blueprint.route("/bidding/<item_id>", methods=["GET"])
@login_required
def bidding(item_id):
    bid = Bid.query.get(item_id)
    return render_template("bidding.html", bid=bid)

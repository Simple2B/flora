from flask import Blueprint, render_template, session, redirect, url_for, request
from flask_login import login_required
from flask import current_app
from app.procore import ProcoreApi

from app.models import Bid

bidding_blueprint = Blueprint("bidding", __name__)


@bidding_blueprint.route("/procore/redirect")
def procore():
    auth_token = request.args["code"]
    session["procore_auth_token"] = auth_token
    return redirect(url_for("bidding.biddings"))


@bidding_blueprint.route("/biddings")
@login_required
def biddings():
    if current_app.config["TESTING"]:
        papi = ProcoreApi()
        bids_from_procore = papi.bids()
        bids = Bid.query.all()
        for bid in bids_from_procore:
            if bid["bid_package_id"] not in [i.procore_bid_id for i in bids]:
                bidding = Bid(
                    procore_bid_id=bid["bid_package_id"],
                    title=bid["bid_package_title"],
                    client=bid["name"],
                    status="New",
                )
                bidding.save()
        bids = Bid.query.all()
        return render_template("biddings.html", bids=bids)

    papi = ProcoreApi()

    if not session.get("procore_access_token", None):
        auth_token = session.get("procore_auth_token", None)
        if not auth_token:
            return redirect(url_for("procore.procore_auth"))
        access_token, refresh_token, created_at = papi.get_token(auth_token)
        session["procore_access_token"] = access_token
        session["procore_refresh_token"] = refresh_token

    papi.access_token = session.get("procore_access_token", None)
    bids_from_procore = papi.bids()

    # assert bids_from_procore
    for bid in bids_from_procore:
        db_bid = Bid.query.filter(Bid.procore_bid_id == bid["bid_package_id"]).first()
        if not db_bid:
            bidding = Bid(
                procore_bid_id=bid["bid_package_id"],
                title=bid["bid_package_title"],
                client=bid["vendor"]["name"]
            )
            bidding.save()

    bids = Bid.query.order_by(Bid.status).all()

    return render_template("biddings.html", bids=bids)


@bidding_blueprint.route("/bidding/<item_id>", methods=["GET"])
@login_required
def bidding(item_id):
    bid = Bid.query.get(item_id)
    return render_template("bidding.html", bid=bid)

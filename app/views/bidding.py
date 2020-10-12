from flask import Blueprint, render_template, session, redirect, url_for, request
from flask_login import login_required
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
    papi = ProcoreApi()
    if not session.get("procore_access_token", None):
        auth_token = session.get("procore_auth_token", None)
        access_token, refresh_token, created_at = papi.get_token(auth_token)
        session["procore_access_token"] = access_token
        session["procore_refresh_token"] = refresh_token

    papi.access_token = session.get("procore_access_token", None)
    bids = Bid.query.all()
    # TODO: read biddings from procore and update DB
    # TODO: add to module procore_id
    bids_from_procore = papi.bids()
    assert bids_from_procore
    for bid in bids_from_procore:
        if bid["bid_package_id"] not in [i.id for i in bids]:
            bidding = Bid(
                id=bid["bid_package_id"],
                title=bid["bid_package_title"],
                client=bid["vendor"]["name"],
                status="New",
            )
            bidding.save()
    return render_template("biddings.html", bids=bids)


@bidding_blueprint.route("/bidding/<item_id>", methods=["GET"])
@login_required
def bidding(item_id):
    bid = Bid.query.get(item_id)
    return render_template("bidding.html", bid=bid)

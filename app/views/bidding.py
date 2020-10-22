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
        bid_package_id = bid["bid_package_id"]
        db_bid = Bid.query.filter(Bid.procore_bid_id == bid_package_id).first()
        if not db_bid:
            bidding = Bid(
                procore_bid_id=bid["bid_package_id"],
                title=bid["bid_package_title"],
                client=bid["vendor"]["name"],
            )
            bidding.save()

    bids = Bid.query.order_by(Bid.status).all()

    return render_template("biddings.html", bids=bids)


@bidding_blueprint.route("/bidding/<int:bid_id>", methods=["GET"])
@login_required
def bidding(bid_id):
    bid = Bid.query.get(bid_id)
    work_items_ides = [
        link_work_item.work_item_id for link_work_item in bid.link_work_items
    ]
    list_work_items = []
    for work_item_id in work_items_ides:
        list_work_items += [WorkItem.query.get(work_item_id)]
    show_exclusions = (", ").join(
        [exclusion_link.exclusion.title for exclusion_link in bid.exclusion_links]
    ) + "."
    show_exclusions = show_exclusions.capitalize()
    show_clarifications = (", ").join(
        [
            clarification_link.clarification.note
            for clarification_link in bid.clarification_links
        ]
    ) + "."
    show_clarifications = show_clarifications.capitalize()
    return render_template(
        "bidding.html",
        bid=bid,
        list_work_items=list_work_items,
        show_exclusions=show_exclusions,
        show_clarifications=show_clarifications,
    )


@bidding_blueprint.route("/delete_exclusions/<int:bid_id>")
@login_required
def delete_exclusions(bid_id):
    bid = Bid.query.get(bid_id)
    for exclusion_link in bid.exclusion_links:
        exclusion_link.delete()
    return redirect(url_for("bidding.bidding", bid_id=bid_id, _anchor="bid_exclusion"))


@bidding_blueprint.route("/edit_exclusions/<int:bid_id>")
@login_required
def edit_exclusions(bid_id):
    return redirect(url_for("exclusion.exclusions", bid_id=bid_id))


@bidding_blueprint.route("/delete_clarifications/<int:bid_id>")
@login_required
def delete_clarifications(bid_id):
    bid = Bid.query.get(bid_id)
    for clarification_link in bid.clarification_links:
        clarification_link.delete()
    return redirect(
        url_for("bidding.bidding", bid_id=bid_id, _anchor="bid_clarification")
    )


@bidding_blueprint.route("/edit_clarifications/<int:bid_id>")
@login_required
def edit_clarifications(bid_id):
    return redirect(url_for("clarification.clarifications", bid_id=bid_id))

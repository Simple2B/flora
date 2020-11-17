import datetime
import time
from flask import Blueprint, render_template, redirect, url_for, session, request
from flask_login import login_required
from flask import current_app
from flask_wtf import FlaskForm

from app.procore import ProcoreApi

from app.models import Bid
from app.logger import log


bidding_blueprint = Blueprint("bidding", __name__)


@bidding_blueprint.route("/edit_bid")
@login_required
def edit_bid():
    session["edit_bid"] = True
    return redirect(url_for("bidding.biddings"))


@bidding_blueprint.route("/finish_edit_bid")
@login_required
def finish_edit_bid():
    session["edit_bid"] = False
    return redirect(url_for("bidding.biddings"))


@bidding_blueprint.route("/edited_bids", methods=["GET", "POST"])
@login_required
def edited_bids():
    FlaskForm(request.form)
    bids_list = [int(bid_id) for bid_id in request.form if request.form.get(bid_id, '') == 'on']
    for bid_id in bids_list:
        bid = Bid.query.get(bid_id)
        bid.status = Bid.Status.d_archived
        bid.save()
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

    # Take bids
    papi = ProcoreApi()
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

    edit_bid = session.get('edit_bid', False)

    status_active_all = session.get("status_active_all", "status-active")
    status_active_submitted = session.get("status_active_submitted", "")
    status_active_archived = session.get("status_active_archived", "")
    status_active_draft = session.get("status_active_draft", "")

    if status_active_submitted:
        bids = Bid.query.filter(Bid.status == Bid.Status.c_submitted).all()
    elif status_active_archived:
        bids = Bid.query.filter(Bid.status == Bid.Status.d_archived).all()
    elif status_active_draft:
        bids = Bid.query.filter(Bid.status == Bid.Status.b_draft).all()
    else:
        bids = Bid.query.order_by(Bid.status).all()
        time_now = round(time.time())
        for bid in bids:
            if bid.time_updated != 0.0:
                bid.last_updated = f'{time_now - bid.time_updated} ago'
                bid.save()

    date_today = datetime.datetime.today().strftime("%m/%d/%Y")
    return render_template(
        "biddings.html",
        bids=bids,
        edit_bid=edit_bid,
        date_today=date_today,
        status_active_all=status_active_all,
        status_active_submitted=status_active_submitted,
        status_active_archived=status_active_archived,
        status_active_draft=status_active_draft,
    )


@bidding_blueprint.route("/change_status", methods=["POST"])
@login_required
def change_status():
    form = FlaskForm(request.form)
    if form.validate_on_submit():
        session["status_active_draft"] = ""
        session["status_active_submitted"] = ""
        session["status_active_archived"] = ""
        session["status_active_all"] = ""
        if request.form["bids_status"] == "Draft":
            session["status_active_draft"] = "status-active"
        elif request.form["bids_status"] == "Submitted":
            session["status_active_submitted"] = "status-active"
        elif request.form["bids_status"] == "Archived":
            session["status_active_archived"] = "status-active"
        else:
            session["status_active_all"] = "status-active"
        return redirect(url_for("bidding.biddings"))
    elif form.is_submitted():
        log(log.INFO, "Form submitted")
    return redirect(url_for("bidding.biddings"))


@bidding_blueprint.route("/delete_exclusions/<int:bid_id>")
@login_required
def delete_exclusions(bid_id):
    bid = Bid.query.get(bid_id)
    for exclusion_link in bid.exclusion_links:
        exclusion_link.delete()
    return redirect(url_for("bid.bidding", bid_id=bid_id, _anchor="bid_exclusion"))


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
    return redirect(url_for("bid.bidding", bid_id=bid_id, _anchor="bid_clarification"))


@bidding_blueprint.route("/edit_clarifications/<int:bid_id>")
@login_required
def edit_clarifications(bid_id):
    return redirect(url_for("clarification.clarifications", bid_id=bid_id))

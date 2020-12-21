import time
import zipfile
from io import BytesIO

from datetime import datetime
from flask import Blueprint, render_template, redirect, url_for, session, request, send_file
from flask_login import login_required
from flask import current_app
from flask_wtf import FlaskForm

from app.procore import ProcoreApi
from app.models import Bid
from app.logger import log
from app.controllers import create_pdf_file

bidding_blueprint = Blueprint("bidding", __name__)


@bidding_blueprint.route("/finish_edit_bid")
@login_required
def finish_edit_bid():
    session["edit_bid"] = False
    return redirect(url_for("bidding.biddings"))


@bidding_blueprint.route("/edit_bid")
@login_required
def edit_bid():
    session["edit_bid"] = True
    return redirect(url_for("bidding.biddings"))


@bidding_blueprint.route("/archive_or_export", methods=["POST"])
@login_required
def archive_or_export():
    FlaskForm(request.form)
    bid_ides_list = [int(bid_id) for bid_id in request.form if request.form.get(bid_id, '') == 'on']
    if request.form.get('arcive', ''):
        for bid_id in bid_ides_list:
            bid = Bid.query.get(bid_id)
            bid.status = Bid.Status.d_archived
            bid.save()
    elif request.form.get('multiply_export', ''):
        stream_of_bids = []
        for bid_id in bid_ides_list:
            bid = Bid.query.get(bid_id)
            stream = create_pdf_file(bid_id)
            stream_of_bids += [(f'bidding_{bid.procore_bid_id}', stream)]
            log(log.INFO, f"Sending file({type(stream)})")

        zipped_file = BytesIO()
        with zipfile.ZipFile(zipped_file, 'w') as zip:
            for i in stream_of_bids:
                stream.seek(0)
                zip.writestr(f"{i[0]}.pdf", i[1].read())
        zipped_file.seek(0)

        now = datetime.datetime.now()
        return send_file(
            zipped_file,
            as_attachment=True,
            attachment_filename="bids_pdf.zip",
            mimetype="application/zip",
            cache_timeout=0,
            last_modified=now,
        )
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

    most_popular = session.get("most_popular", "")
    most_recent = session.get("most_recent", "Most recent")

    edit_bid = session.get('edit_bid', False)

    status_active_all = session.get("status_active_all", "status-active")
    status_active_submitted = session.get("status_active_submitted", "")
    status_active_archived = session.get("status_active_archived", "")
    status_active_draft = session.get("status_active_draft", "")

    if status_active_submitted:
        bids = Bid.query.filter(Bid.status == Bid.Status.c_submitted).all()
        if most_recent:
            bids = Bid.query.filter(Bid.status == Bid.Status.c_submitted).order_by(Bid.time_updated).all()
            bids.reverse()
    elif status_active_archived:
        bids = Bid.query.filter(Bid.status == Bid.Status.d_archived).all()
        if most_recent:
            bids = Bid.query.filter(Bid.status == Bid.Status.d_archived).order_by(Bid.time_updated).all()
            bids.reverse()
    elif status_active_draft:
        bids = Bid.query.filter(Bid.status == Bid.Status.b_draft).all()
        if most_recent:
            bids = Bid.query.filter(Bid.status == Bid.Status.b_draft).order_by(Bid.time_updated).all()
            bids.reverse()
    else:
        bids = Bid.query.order_by(Bid.status).all()
        if most_recent:
            bids = Bid.query.order_by(Bid.time_updated).all()
            bids.reverse()

    time_now = round(time.time())
    for bid in bids:
        if bid.time_updated != 0.0:
            seconds_ago = int(time_now - bid.time_updated)
            if seconds_ago < 3600:
                if seconds_ago <= 60:
                    bid.last_updated = '1 min ago'
                    bid.save()
                else:
                    bid.last_updated = f'{seconds_ago // 60} mins ago'
                    bid.save()
            elif seconds_ago >= 3600 and seconds_ago < 86400:
                bid.last_updated = f'{seconds_ago // 3600} hours ago'
                bid.save()
            elif seconds_ago >= 86400 and seconds_ago < 2073600:
                bid.last_updated = f'{seconds_ago // 86400} days ago'
                bid.save()
            else:
                bid.last_updated = time.strftime("%m/%d/%Y", time.gmtime(bid.time_updated))
                bid.save()

    today_date = datetime.today().strftime("%m/%d/%Y")
    return render_template(
        "biddings.html",
        bids=bids,
        edit_bid=edit_bid,
        today_date=today_date,
        most_popular=most_popular,
        most_recent=most_recent,
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


@bidding_blueprint.route("/select_sort", methods=["POST"])
@login_required
def select_sort():
    if request.form.get("select_sort", "") == "Most recent":
        session["most_recent"] = "Most recent"
        session["most_popular"] = ""
    elif request.form.get("select_sort", "") == "Most popular":
        session["most_popular"] = "Most popular"
        session["most_recent"] = ""
    return redirect(url_for("bidding.biddings"))

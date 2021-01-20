import time
import zipfile
from io import BytesIO
from datetime import datetime

from flask import Blueprint, render_template, redirect, url_for, session, request, send_file
from flask_login import login_required
from flask_wtf import FlaskForm
from sqlalchemy import desc

from app.models import Bid
from app.forms import BidForm
from app.logger import log
from app.controllers import create_pdf_file, create_docx

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
    form = BidForm(request.form)
    bid_ides_list = [int(bid_id) for bid_id in request.form if request.form.get(bid_id, '') == 'on']
    if request.form.get('arcive', ''):
        for bid_id in bid_ides_list:
            bid = Bid.query.get(bid_id)
            bid.status = Bid.Status.d_archived
            bid.save()
    elif form.data['export_pdf']:
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

        now = datetime.now()
        return send_file(
            zipped_file,
            as_attachment=True,
            attachment_filename="bids_pdf.zip",
            mimetype="application/zip",
            cache_timeout=0,
            last_modified=now,
        )
    elif form.data['export_docx']:
        stream_of_bids = []
        for bid_id in bid_ides_list:
            bid = Bid.query.get(bid_id)
            create_docx(bid_id)
        zipped_file = BytesIO()
            with zipfile.ZipFile(zipped_file, 'w') as zip:
                pass
        with open('test_docx.docx', 'rb') as f:
            stream = BytesIO(f.read())
        now = datetime.now()
        # return None
        return send_file(
            stream,
            # as_attachment=True,
            attachment_filename="test_docx.docx",
            mimetype="application/msword",
            cache_timeout=0,
            last_modified=now,
        )
    return redirect(url_for("bidding.biddings"))


@bidding_blueprint.route("/biddings")
@login_required
def biddings():
    form = BidForm()
    most_popular = session.get("most_popular", "")
    most_recent = session.get("most_recent", "Most recent")
    edit_bid = session.get('edit_bid', False)

    status_active_all = session.get("status_active_all", "status-active")
    status_active_submitted = session.get("status_active_submitted", "")
    status_active_archived = session.get("status_active_archived", "")
    status_active_draft = session.get("status_active_draft", "")

    bids_query = Bid.query
    if status_active_submitted:
        bids_query = bids_query.filter(Bid.status == Bid.Status.c_submitted)
    elif status_active_archived:
        bids_query = bids_query.filter(Bid.status == Bid.Status.d_archived)
    elif status_active_draft:
        bids_query = bids_query.filter(Bid.status == Bid.Status.b_draft)
    bids_query = bids_query.order_by(desc(Bid.time_updated if most_recent else Bid.popularity))

    bids = bids_query.all()

    time_now = round(time.time())
    for bid in bids:
        if bid.time_updated != 0.0:
            seconds_ago = int(time_now - bid.time_updated)
            if seconds_ago < 3600:
                if seconds_ago <= 60:
                    bid.last_updated = '1 min ago'
                else:
                    bid.last_updated = f'{seconds_ago // 60} mins ago'
            elif seconds_ago >= 3600 and seconds_ago < 86400:
                bid.last_updated = f'{seconds_ago // 3600} hours ago'
            elif seconds_ago >= 86400 and seconds_ago < 2073600:
                bid.last_updated = f'{seconds_ago // 86400} days ago'
            else:
                bid.last_updated = time.strftime("%m/%d/%Y", time.gmtime(bid.time_updated))

    today_date = datetime.today().strftime("%m/%d/%Y")
    return render_template(
        "biddings.html",
        bids=bids,
        form=form,
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

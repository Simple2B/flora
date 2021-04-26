import os
import time
import zipfile
from io import BytesIO
from datetime import datetime

from flask import Blueprint, render_template, redirect, url_for, session, request, send_file
from flask_login import login_required
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


@bidding_blueprint.route("/archive_or_export", methods=["GET", "POST"])
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
            stream_of_bids += [(f'pdf_bid_{bid.procore_bid_id}', stream)]
            log(log.DEBUG, "Sending pdf file([%s])", stream)

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
            filepath = create_docx(bid_id)
            stream = None
            with open(filepath, 'rb') as f:
                stream = BytesIO(f.read())
            os.remove(filepath)
            if not stream:
                log(log.ERROR, "archive_or_export() cannot open [%s]", filepath)
                return redirect(url_for("bidding.biddings"))
            stream_of_bids += [(f'pdf_bid_{bid.procore_bid_id}', stream)]
            log(log.DEBUG, "Sending docx file([%s])", stream)
        zipped_file = BytesIO()
        with zipfile.ZipFile(zipped_file, 'w') as zip:
            for i in stream_of_bids:
                stream.seek(0)
                zip.writestr(f"{i[0]}.docx", i[1].read())
        zipped_file.seek(0)
        now = datetime.now()
        return send_file(
            zipped_file,
            as_attachment=True,
            attachment_filename="bids_docx.zip",
            mimetype="application/zip",
            cache_timeout=0,
            last_modified=now,
        )
    return redirect(url_for("bidding.biddings"))


@bidding_blueprint.route("/biddings", methods=["GET"])
@login_required
def biddings():
    form = BidForm()
    sort_by = request.args.get("select_sort", "")
    due_date = "due_date"
    bidding_id = "bidding_id"
    if sort_by == due_date:
        sort_by = Bid.due_date
        bidding_id = ""
    elif sort_by == bidding_id:
        sort_by = ""
        due_date = ""
    else:
        sort_by = Bid.time_updated
        due_date = ""
        bidding_id = ""

    edit_bid = session.get('edit_bid', False)

    status_active_submitted = request.args.get("Submitted", "")
    status_active_archived = request.args.get("Archived", "")
    status_active_draft = request.args.get("Draft", "")
    status_active_new = request.args.get("New", "")

    if status_active_submitted or status_active_archived or status_active_draft:
        status_active_all = ""
    else:
        status_active_all = "status-active"

    bids_query = Bid.query
    if status_active_submitted:
        bids_query = bids_query.filter(Bid.status == Bid.Status.c_submitted)
    elif status_active_archived:
        bids_query = bids_query.filter(Bid.status == Bid.Status.d_archived)
    elif status_active_draft:
        bids_query = bids_query.filter(Bid.status == Bid.Status.b_draft)
    elif status_active_new:
        bids_query = bids_query.filter(Bid.status == Bid.Status.a_new)

    bids_query = bids_query.order_by(desc(sort_by) if sort_by else Bid.procore_bid_id)

    bids = bids_query.all()
    # bids.status.value

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
        due_date=due_date,
        bidding_id=bidding_id,
        status_active_all=status_active_all,
        status_active_submitted=status_active_submitted,
        status_active_archived=status_active_archived,
        status_active_draft=status_active_draft,
        status_active_new=status_active_new,
    )

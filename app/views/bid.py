from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required

from app.models import Bid, WorkItem
from app.models import WorkItemLine, LinkWorkItem

from app.forms import WorkItemLineForm

bid_blueprint = Blueprint("bid", __name__)


@bid_blueprint.route(
    "/add_work_item_line/<bid_id>/<int:link_work_item_id>", methods=["GET", "POST"]
)
@login_required
def add_work_item_line(bid_id, link_work_item_id):
    form = WorkItemLineForm()
    # if form.validate_on_submit():
    #     WorkItemLine(link_work_items_id=link_work_item_id).save()
    return redirect(url_for("bid.bidding", bid_id=bid_id))


@bid_blueprint.route("/bidding/<int:bid_id>", methods=["GET"])
@login_required
def bidding(bid_id):
    bid = Bid.query.get(bid_id)
    form = WorkItemLineForm()
    return render_template(
        "bidding.html",
        bid=bid,
        form=form
    )

from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required

from app.models import Bid
from app.models import WorkItemLine, LinkWorkItem

from app.forms import WorkItemLineForm

from app.logger import log

bid_blueprint = Blueprint("bid", __name__)


@bid_blueprint.route(
    "/add_work_item_line/<bid_id>/<int:link_work_item_id>", methods=["GET"]
)
@login_required
def add_work_item_line(bid_id, link_work_item_id):
    WorkItemLine(link_work_items_id=link_work_item_id).save()
    return redirect(url_for("bid.bidding", bid_id=bid_id))


@bid_blueprint.route(
    "/edit_work_item_line/<int:bid_id>/<int:work_item_line_id>", methods=["POST"]
)
@login_required
def edit_work_item_line(bid_id, work_item_line_id):
    form = WorkItemLineForm()
    if form.validate_on_submit():
        line = WorkItemLine.query.get(work_item_line_id)
        if line:
            line.note = form.note.data
            line.description = form.description.data
            line.price = form.price.data
            line.unit = form.unit.data
            line.quantity = form.quantity.data
            line.tbd = form.tbd.data
            line.save()
        else:
            log(log.ERROR, "Unknown work_item_line_id: %d", work_item_line_id)

    return redirect(url_for("bid.bidding", bid_id=bid_id, _anchor='bid_scope_of_work'))


@bid_blueprint.route(
    "/delete_link_work_item/<int:bid_id>/<int:link_work_item_id>", methods=["GET"]
)
@login_required
def delete_link_work_item(bid_id, link_work_item_id):
    line = LinkWorkItem.query.get(link_work_item_id)
    if line:
        line.delete()
    else:
        log(log.ERROR, "Unknown work_item_line_id: %d", link_work_item_id)
    return redirect(url_for("bid.bidding", bid_id=bid_id, _anchor='bid_scope_of_work'))


@bid_blueprint.route(
    "/delete_work_item_line/<int:bid_id>/<int:work_item_line_id>", methods=["GET"]
)
@login_required
def delete_work_item_line(bid_id, work_item_line_id):
    line = WorkItemLine.query.get(work_item_line_id)
    if line:
        line.delete()
    else:
        log(log.ERROR, "Unknown work_item_line_id: %d", work_item_line_id)
    return redirect(url_for("bid.bidding", bid_id=bid_id, _anchor='bid_scope_of_work'))


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

from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required

from app.models import Bid, WorkItem

bid_blueprint = Blueprint("bid", __name__)


@bid_blueprint.route("/bidding/<int:item_id>", methods=["GET"])
@login_required
def add_work_item_line(item_id):
    bid = Bid.query.get(item_id)
    return redirect(url_for("bidding.html", bid=bid))


@bid_blueprint.route("/bidding/<int:item_id>", methods=["GET"])
@login_required
def bidding(item_id):
    bid = Bid.query.get(item_id)
    work_items_ides = [link_work_item.work_item_id for link_work_item in bid.link_work_items]
    list_work_items = []
    for work_item_id in work_items_ides:
        list_work_items += [WorkItem.query.get(work_item_id)]
    return render_template("bidding.html", bid=bid, list_work_items=list_work_items)

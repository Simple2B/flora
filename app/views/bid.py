from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required

from app.models import Bid, WorkItemLine, LinkWorkItem, WorkItem

from app.forms import WorkItemLineForm

from app.controllers import calculate_subtotal

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
    link = LinkWorkItem.query.get(link_work_item_id)
    if link:
        for line in link.work_item_lines:
            line.delete()
        link.delete()
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


@bid_blueprint.route("/delete_exclusions/<int:bid_id>")
@login_required
def delete_exclusions(bid_id):
    bid = Bid.query.get(bid_id)
    for exclusion_link in bid.exclusion_links:
        exclusion_link.delete()
    return redirect(url_for("bidding.bidding", bid_id=bid_id, _anchor="bid_exclusion"))


@bid_blueprint.route("/edit_exclusions/<int:bid_id>")
@login_required
def edit_exclusions(bid_id):
    return redirect(url_for("exclusion.exclusions", bid_id=bid_id))


@bid_blueprint.route("/delete_clarifications/<int:bid_id>")
@login_required
def delete_clarifications(bid_id):
    bid = Bid.query.get(bid_id)
    for clarification_link in bid.clarification_links:
        clarification_link.delete()
    return redirect(
        url_for("bid.bidding", bid_id=bid_id, _anchor="bid_clarification")
    )


@bid_blueprint.route("/edit_clarifications/<int:bid_id>")
@login_required
def edit_clarifications(bid_id):
    return redirect(url_for("clarification.clarifications", bid_id=bid_id))


@bid_blueprint.route("/bidding/<int:bid_id>", methods=["GET"])
@login_required
def bidding(bid_id):
    bid = Bid.query.get(bid_id)
    form = WorkItemLineForm()
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
    calculate_subtotal(bid_id)

    return render_template(
        "bidding.html",
        bid=bid,
        form=form,
        show_exclusions=show_exclusions,
        show_clarifications=show_clarifications
    )

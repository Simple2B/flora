from flask import Blueprint, render_template, url_for, redirect, request, session
from flask_login import login_required

from app.models import Exclusion, Bid, ExclusionLink
from app.forms import ExclusionForm, ExclusionCartForm

exclusion_blueprint = Blueprint("exclusion", __name__)


@exclusion_blueprint.route("/add_new_exclusion/<bid_id>", methods=["POST"])
@login_required
def add_new_exclusion(bid_id):
    form = ExclusionForm(request.form)
    if form.validate_on_submit():
        # if add_work_item_validator(
        #     form.code.data,
        # ):
        exclusion = Exclusion(
            title=form.title.data,
        )
        exclusion.save()
        # flash("Registration successful. You are logged in.", "success")
        return redirect(url_for("exclusion.exclusions", bid_id=bid_id))
        # else:
        #     flash("The given data was invalid.", "danger")
        #     return redirect(url_for("work_item.work_items"))
    elif form.is_submitted():
        pass
        # flash("The given data was invalid.", "danger")
    return redirect(url_for("exclusion.exclusions", bid_id=bid_id))


@exclusion_blueprint.route("/add_exclusion_to_cart/<bid_id>", methods=["POST"])
@login_required
def add_exclusion_to_cart(bid_id):
    form = ExclusionCartForm(request.form)
    selected_ids = session.get("SelectedExclusionItemsDict", {})
    form.selected_exclusion_items = {
        int(item_id): Exclusion.query.get(item_id) for item_id in selected_ids
    }
    if form.validate_on_submit():
        form.selected_exclusion_items.update(
            {
                str(k): Exclusion.query.get(int(k))
                for k in request.form
                if request.form[k] == "on"
            }
        )
        session["SelectedExclusionItemsDict"] = {
            str(item_id): item_id for item_id in form.selected_exclusion_items
        }
        return redirect(url_for("exclusion.exclusions", bid_id=bid_id))
    elif form.is_submitted():
        pass
        # flash("The given data was invalid.", "danger")
    return redirect(url_for("exclusion.exclusions", bid_id=bid_id))


@exclusion_blueprint.route(
    "/delete_exclusion_item_from_cart/<bid_id>/<item_id>", methods=["GET"]
)
@login_required
def delete_exclusion_item_from_cart(bid_id, item_id):
    item_id = str(item_id)
    selected_ids = session.get("SelectedExclusionItemsDict", {})
    if item_id in selected_ids:
        del selected_ids[item_id]
    session["SelectedExclusionItemsDict"] = selected_ids
    return redirect(url_for("exclusion.exclusions", bid_id=bid_id))


@exclusion_blueprint.route(
    "/delete_exclusion_item_from_items/<bid_id>/<item_id>", methods=["POST"]
)
@login_required
def delete_exclusion_item_from_items(bid_id, item_id):
    exclusion = Exclusion.query.get(item_id)
    if exclusion:
        selected = session.get("SelectedExclusionItemsDict", {})
        if str(exclusion.id) in selected:
            del selected[str(exclusion.id)]
            session["SelectedExclusionItemsDict"] = selected
        exclusion.delete()
    return redirect(url_for("exclusion.exclusions", bid_id=bid_id))


@exclusion_blueprint.route("/edit_exclusion_item/bid_id/<item_id>", methods=["POST"])
@login_required
def edit_exclusion_item(bid_id, item_id):
    item_id = int(item_id)
    form = ExclusionForm(request.form)
    if form.validate_on_submit():
        exclusion = Exclusion.query.get(item_id)
        if exclusion:
            exclusion.title = form.title.data
            exclusion.save()
    return redirect(url_for("exclusion.exclusions", bid_id=bid_id))


@exclusion_blueprint.route("/exclusions/<bid_id>", methods=["GET"])
@login_required
def exclusions(bid_id):
    form = ExclusionForm(request.form)
    form.exclusions = Exclusion.query.all()
    exclusion_cart_form = ExclusionCartForm()
    selected_exclusion_item_ids = session.get("SelectedExclusionItemsDict", None)
    if selected_exclusion_item_ids is None:
        selected_exclusion_item_ids = {
            str(excl_link.exclusion_id): excl_link.exclusion_id
            for excl_link in ExclusionLink.query.filter(
                ExclusionLink.bid_id == bid_id
            ).all()
        }
        session["SelectedExclusionItemsDict"] = selected_exclusion_item_ids
    exclusion_cart_form.selected_exclusions = [
        Exclusion.query.get(item_id) for item_id in selected_exclusion_item_ids
    ]
    exclusion_cart_form.result_text = ""
    for item in exclusion_cart_form.selected_exclusions:
        if not exclusion_cart_form.result_text:
            exclusion_cart_form.result_text = item.title
        else:
            exclusion_cart_form.result_text += ", "
            exclusion_cart_form.result_text += item.title

    return render_template(
        "exclusions.html",
        form=form,
        exclusion_cart_form=exclusion_cart_form,
        bid_id=bid_id,
    )


@exclusion_blueprint.route("/add_exclusions_to_bid/<int:bid_id>")
@login_required
def add_exclusions_to_bid(bid_id):
    bid = Bid.query.get(bid_id)
    selected_exclusion_item_ids = session.get("SelectedExclusionItemsDict", {})
    for exclusion_link in bid.exclusion_links:
        exclusion_link.delete()
    for selected_exclusion_id in map(int, selected_exclusion_item_ids):
        ExclusionLink(bid_id=bid_id, exclusion_id=selected_exclusion_id).save()
    session["SelectedExclusionItemsDict"] = None
    return redirect(url_for("bidding.bidding", bid_id=bid_id, _anchor='bid_exclusion'))

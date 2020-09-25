from flask import Blueprint, render_template, url_for, redirect, flash, request, session
from flask_login import login_required

from app.models import Clarification
from app.forms import ClarificationForm, ClarificationCartForm

clarification_blueprint = Blueprint("clarification", __name__)


@clarification_blueprint.route("/clarification", methods=["POST"])
@login_required
def clarification():
    form = ClarificationForm(request.form)
    if form.validate_on_submit():
        # if add_work_item_validator(
        #     form.code.data,
        # ):
        clarification = Clarification(
            note=form.note.data,
            description=form.description.data,
        )
        clarification.save()
        flash("Registration successful. You are logged in.", "success")
        return redirect(url_for("clarification.clarifications"))
        # else:
        #     flash("The given data was invalid.", "danger")
        #     return redirect(url_for("clarification.clarifications"))
    elif form.is_submitted():
        flash("The given data was invalid.", "danger")
    return redirect(url_for("clarification.clarifications"))


@clarification_blueprint.route("/add_clarification_item_to_cart", methods=["POST"])
@login_required
def add_clarification_item_to_cart():
    form = ClarificationCartForm(request.form)
    selected_ids = session.get("SelectedClarificationsDict", {})
    form.selected_clarification_items = {
        int(item_id): Clarification.query.get(item_id) for item_id in selected_ids
    }
    if form.validate_on_submit():
        form.selected_clarification_items.update(
            {
                str(k): Clarification.query.get(int(k))
                for k in request.form
                if request.form[k] == "on"
            }
        )
        session["SelectedClarificationsDict"] = {
            str(item_id): item_id for item_id in form.selected_work_items
        }
        return redirect(url_for("work_item.work_items"))
    elif form.is_submitted():
        flash("The given data was invalid.", "danger")
    return redirect(url_for("clarification.clarifications"))


@clarification_blueprint.route(
    "/delete_clarification_item_from_cart/<item_id>", methods=["GET"]
)
@login_required
def delete_clarification_item_from_cart(item_id):
    item_id = str(item_id)
    selected_ids = session.get("SelectedClarificationsDict", {})
    if item_id in selected_ids:
        del selected_ids[item_id]
    session["SelectedClarificationsDict"] = selected_ids
    return redirect(url_for("clarification.clarifications"))


@clarification_blueprint.route("/clarifications", methods=["GET"])
@login_required
def clarifications():
    form = ClarificationForm(request.form)
    clarification_cart_form = ClarificationCartForm()
    selected_clarification_item_ids = session.get("SelectedClarificationsDict", {})
    clarification_cart_form.selected_work_items = [
        Clarification.query.get(item_id) for item_id in selected_clarification_item_ids
    ]
    clarifications = Clarification.query.all()
    return render_template(
        "clarifications.html", form=form, clarifications=clarifications, clarification_cart_form=clarification_cart_form
    )

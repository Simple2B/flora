from flask import Blueprint, render_template, url_for, redirect, flash, request, session
from flask_login import login_required

from app.models import Clarification
from app.forms import ClarificationForm

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


@clarification_blueprint.route("/clarifications", methods=["GET"])
@login_required
def clarifications():
    form = ClarificationForm(request.form)
    clarifications = Clarification.query.all()
    return render_template(
        "clarifications.html", form=form, clarifications=clarifications
    )

from flask import Blueprint, render_template, url_for, redirect, flash, request, session
from flask_login import login_required

from app.models import Exclusion
from app.forms import ExclusionForm

exclusion_blueprint = Blueprint("exclusion", __name__)


@exclusion_blueprint.route("/exclusion", methods=["POST"])
@login_required
def exclusion():
    form = ExclusionForm(request.form)
    if form.validate_on_submit():
        # if add_work_item_validator(
        #     form.code.data,
        # ):
        exclusion = Exclusion(
            title=form.title.data,
            description=form.description.data,
        )
        exclusion.save()
        flash("Registration successful. You are logged in.", "success")
        return redirect(url_for("exclusion.exclusions"))
        # else:
        #     flash("The given data was invalid.", "danger")
        #     return redirect(url_for("work_item.work_items"))
    elif form.is_submitted():
        flash("The given data was invalid.", "danger")
    return redirect(url_for("exclusion.exclusions"))


@exclusion_blueprint.route("/exclusions", methods=["GET"])
@login_required
def exclusions():
    form = ExclusionForm(request.form)
    exclusions = Exclusion.query.all()
    return render_template("exclusions.html", form=form, exclusions=exclusions)

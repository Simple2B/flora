from flask import Blueprint, render_template, url_for, redirect, request, session, flash
from flask_login import login_required

from app.models import Alternate
from app.forms import AlternateForm

alternate_blueprint = Blueprint("alternate", __name__, url_prefix="/alternate")


@alternate_blueprint.route("/new/<int:bid_id>", methods=["POST", "GET"])
@login_required
def new_alternate(bid_id):
    form = AlternateForm()
    if form.validate_on_submit():
        # TODO
        flash("Alternate added successful.", "success")
        return redirect(url_for("bid.bidding", bid_id=bid_id, _anchor="alternates"))
    if form.is_submitted():
        flash("The given data was invalid.", "danger")
    return render_template(
        "alternate.html",
        form=form,
        cancel_url=url_for("bid.bidding", bid_id=bid_id, _anchor="alternates"),
    )


@alternate_blueprint.route(
    "/edit/<int:bid_id>/<int:alternate_id>", methods=["POST", "GET"]
)
@login_required
def edit_alternate(bid_id, alternate_id):
    form = AlternateForm()
    if form.validate_on_submit():
        # TODO
        flash("Alternate added successful.", "success")
        return redirect(url_for("bid.bidding", bid_id=bid_id, _anchor="alternates"))
    elif form.is_submitted():
        pass
        flash("The given data was invalid.", "danger")
    return redirect(url_for("alternate.new_alternate", bid_id=bid_id))


@alternate_blueprint.route("/delete/<int:bid_id>/<int:alternate_id>", methods=["GET"])
@login_required
def delete_alternate(bid_id, alternate_id):
    alternate = Alternate.query.get(alternate_id)
    if alternate:
        alternate.delete()
        flash("Alternate deleted.", "success")
    return redirect(url_for("bid.bidding", bid_id=bid_id, _anchor="alternates"))

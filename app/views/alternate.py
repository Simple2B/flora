from flask import Blueprint, render_template, url_for, redirect, flash
from flask_login import login_required

from app.models import Alternate
from app.forms import AlternateForm
from app.logger import log

alternate_blueprint = Blueprint("alternate", __name__, url_prefix="/alternate")


@alternate_blueprint.route("/new/<int:bid_id>", methods=["POST", "GET"])
@login_required
def new_alternate(bid_id):
    form = AlternateForm()
    if form.validate_on_submit():
        alternate = Alternate(
            bid_id=bid_id,
            name=form.name.data,
            tbd=form.tbd.data,
            description=form.description.data,
            quantity=form.quantity.data,
            unit=form.unit.data,
            price=form.price.data,
        )
        alternate.save()
        log(log.DEBUG, "Alternate added successful.", "success")
        return redirect(url_for("bid.bidding", bid_id=bid_id, _anchor="bid_alternates"))
    elif form.is_submitted():
        log(log.ERROR, "%s", form.errors)
        for error in form.errors:
            for msg in form.errors[error]:
                flash(f"{error}: {msg}", "warning")
    return render_template(
        "alternate.html",
        form=form,
        cancel_url=url_for("bid.bidding", bid_id=bid_id, _anchor="bid_alternates"),
    )


@alternate_blueprint.route(
    "/edit/<int:bid_id>/<int:alternate_id>", methods=["POST", "GET"]
)
@login_required
def edit_alternate(bid_id, alternate_id):
    form = AlternateForm()
    alternate = Alternate.query.get(alternate_id)
    if form.validate_on_submit():
        alternate.name = form.name.data
        alternate.tbd = form.tbd.data
        alternate.description = form.description.data
        alternate.quantity = form.quantity.data
        alternate.unit = form.unit.data
        alternate.price = form.price.data
        alternate.save()
        log(log.DEBUG, "Alternate added successful.", "success")
        return redirect(url_for("bid.bidding", bid_id=bid_id, _anchor="bid_alternates"))
    elif form.is_submitted():
        for error in form.errors:
            for msg in form.errors[error]:
                log(log.ERROR, "edit_alternate(): %s", msg)
                flash(msg, "warning")
    form.name.data = alternate.name
    form.tbd.data = alternate.tbd
    form.description.data = alternate.description
    form.quantity.data = alternate.quantity
    form.unit.data = alternate.unit
    form.price.data = alternate.price
    return render_template(
        "alternate.html",
        form=form,
        cancel_url=url_for("bid.bidding", bid_id=bid_id, _anchor="bid_alternates"),
    )


@alternate_blueprint.route("/delete/<int:bid_id>/<int:alternate_id>", methods=["GET"])
@login_required
def delete_alternate(bid_id, alternate_id):
    alternate = Alternate.query.get(alternate_id)
    if alternate:
        alternate.delete()
        flash("Alternate deleted.", "success")
    return redirect(url_for("bid.bidding", bid_id=bid_id, _anchor="bid_alternates"))

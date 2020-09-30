from flask import render_template, Blueprint, redirect, url_for, request, session
from flask_login import login_required

from app.forms import RegistrationForm
from app.models import User, WorkItem
from app.procore import ProcoreApi


main_blueprint = Blueprint("main", __name__)


@main_blueprint.route("/")
@login_required
def index():
    return render_template("index.html")


@main_blueprint.route("/biddings")
@login_required
def biddings():
    # TODO: need refactoring!
    work_items = WorkItem.query.all()
    test = ["12345", "test", "test", "test", "test", "test", "test", "test"]
    return render_template("biddings.html", work_items=work_items, test=test)


@main_blueprint.route("/bidding/<item_id>", methods=["GET"])
@login_required
def bidding(item_id):
    item_id = item_id
    return render_template("bidding.html", item_id=item_id)


@main_blueprint.route("/team")
@login_required
def team():
    form = RegistrationForm(request.form)
    users = User.query.all()
    return render_template("team.html", form=form, users=users)


@main_blueprint.route("/resources")
@login_required
def resources():
    return render_template("header.html")


@main_blueprint.route("/header")
@login_required
def header():
    return render_template("header.html")


@main_blueprint.route("/test")
def test():
    return redirect(url_for("main.bidding/#work-item-container"))

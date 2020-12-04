from flask import render_template, Blueprint, redirect, url_for
from flask_login import login_required


main_blueprint = Blueprint("main", __name__)


@main_blueprint.route("/")
@login_required
def index():
    return render_template("index.html")


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
    return redirect(url_for("bidding.bidding/#work-item-container"))

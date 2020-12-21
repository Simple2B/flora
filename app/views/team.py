from flask import render_template, Blueprint, redirect, url_for, request
from flask_login import login_required

from app.forms import RegistrationForm
from app.models import User

team_blueprint = Blueprint("team", __name__)


@team_blueprint.route("/edit_card/<int:user_id>", methods=["POST"])
@login_required
def edit_card(user_id):
    form = RegistrationForm(request.form)
    user = User.query.get(user_id)
    user.username = form.username.data
    user.email = form.email.data
    user.position = form.position.data
    user.phone = form.phone.data
    user.password = form.password.data
    user.save()
    return redirect(url_for("team.team"))


@team_blueprint.route("/delete_card/<int:user_id>")
@login_required
def delete_card(user_id):
    user = User.query.get(user_id)
    user.delete()
    return redirect(url_for("team.team"))


@team_blueprint.route("/team")
@login_required
def team():
    form = RegistrationForm(request.form)
    users = User.query.all()
    return render_template("team.html", form=form, users=users)

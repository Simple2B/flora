from flask import render_template, Blueprint, redirect, url_for, request, flash
from flask_login import login_required

from app.forms import EditUserForm, RegistrationForm
from app.models import User

from app.logger import log

team_blueprint = Blueprint("team", __name__)


@team_blueprint.route("/edit_card/<int:user_id>", methods=["POST"])
@login_required
def edit_card(user_id):
    form = EditUserForm(request.form)
    if form.validate_on_submit():
        user = User.query.get(user_id)
        user.username = form.username.data
        user.email = form.email.data
        user.position = form.position.data
        user.phone = form.phone.data
        user.password = form.password.data
        user.save()
        # flash(f"User '{user.username}' changed", "success")
    elif form.is_submitted():
        log(log.ERROR, "edit_card(): %s", form.errors)
        for error in form.errors:
            for msg in form.errors[error]:
                flash(f"{msg}", "warning")
    return redirect(url_for("team.team"))


@team_blueprint.route("/delete_card/<int:user_id>")
@login_required
def delete_card(user_id):
    user = User.query.get(user_id)
    user.delete()
    return redirect(url_for("team.team"))


@team_blueprint.route("/team", methods=["GET"])
@login_required
def team():
    form = RegistrationForm(request.form)
    users = User.query.all()
    return render_template("team.html", form=form, users=users)

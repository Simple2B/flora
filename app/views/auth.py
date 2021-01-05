from flask import Blueprint, render_template, url_for, redirect, flash, request, session
from flask_login import login_user, login_required

from app.models import User
from app.forms import LoginForm, RegistrationForm
from app.controllers import add_user_data_validator

auth_blueprint = Blueprint("auth", __name__)


@auth_blueprint.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit() or form.data['submit']:
        if add_user_data_validator(
            form.username.data,
            form.email.data,
            form.phone.data,
        ):
            user = User(
                username=form.username.data,
                email=form.email.data,
                user_type=form.user_type.data,
                position=form.position.data,
                phone=form.phone.data,
                password=form.password.data,
            )
            user.save()
            flash("Registration successful. You are logged in.", "success")
            return redirect(url_for("team.team"))
        else:
            flash("The given data was invalid.", "danger")
            return redirect(url_for("team.team"))
    elif form.is_submitted():
        flash("The given data was invalid.", "danger")
    return redirect(url_for("team.team"))


@auth_blueprint.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm(request.form)
    if form.validate_on_submit():
        user = User.authenticate(form.user_id.data, form.password.data)
        if user is not None:
            login_user(user)
            flash("Login successful.", "success")
            return redirect(url_for("team.team"))
        flash("Wrong user login/email or password.", "danger")
    return render_template("auth/login.html", form=form)


@auth_blueprint.route("/logout")
@login_required
def logout():
    session.clear()
    flash("You were logged out.", "info")
    return redirect(url_for("auth.login"))

from flask import Blueprint, render_template, url_for, redirect, flash, request
from flask_login import login_user, logout_user, login_required

from app.models import User, WorkItem
from app.forms import LoginForm, RegistrationForm, WorkItemForm
from app.controllers import add_user_data_validator, add_work_item_validator

auth_blueprint = Blueprint("auth", __name__)


@auth_blueprint.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm(request.form)
    if form.validate_on_submit():
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
            return redirect(url_for("main.team"))
        else:
            flash("The given data was invalid.", "danger")
            return redirect(url_for("main.team"))
    elif form.is_submitted():
        flash("The given data was invalid.", "danger")
    return redirect(url_for("main.team"))


@auth_blueprint.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm(request.form)
    if form.validate_on_submit():
        user = User.authenticate(form.user_id.data, form.password.data)
        if user is not None:
            login_user(user)
            flash("Login successful.", "success")
            return redirect(url_for("main.team"))
        flash("Wrong user login/email or password.", "danger")
    return render_template("auth/login.html", form=form)


@auth_blueprint.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You were logged out.", "info")
    return redirect(url_for("auth.login"))


@auth_blueprint.route("/work_item", methods=["GET", "POST"])
def work_item():
    form = WorkItemForm(request.form)
    if form.validate_on_submit():
        if add_work_item_validator(
            form.code.data,
        ):
            work_item = WorkItem(
                name=form.name.data,
                code=form.code.data,
            )
            work_item.save()
            flash("Registration successful. You are logged in.", "success")
            return redirect(url_for("main.bidding"))
        else:
            flash("The given data was invalid.", "danger")
            return redirect(url_for("main.bidding"))
    elif form.is_submitted():
        flash("The given data was invalid.", "danger")
    return redirect(url_for("main.bidding"))

from flask import Blueprint, render_template, redirect, request, flash
from flask_login import login_required, current_user

from app.forms import ProfileForm
from app.logger import log


profile_blueprint = Blueprint("profile", __name__)


@profile_blueprint.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    form = ProfileForm()
    next_url = request.args.get('next_link', '/')
    log(log.DEBUG, 'Next URL : [%s]', next_url)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.position = form.position.data
        current_user.phone = form.phone.data
        if form.password.data:
            current_user.password = form.password.data
        current_user.save()
        log(log.DEBUG, 'Form validate with succeed!')
        return redirect(f'{next_url}')
    if form.is_submitted():
        log(log.ERROR, "%s", form.errors)
        for error in form.errors:
            for msg in form.errors[error]:
                flash(msg, "warning")

    return render_template(
        "profile.html",
        form=form,
        user=current_user,
        previous_route=next_url
    )

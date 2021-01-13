from flask import Blueprint, render_template, redirect, request, url_for, session
from flask_login import login_required

from app.logger import log


profile_blueprint = Blueprint("profile", __name__)


@profile_blueprint.route("/get_window_location_link/", methods=["GET", "POST"])
@login_required
def get_window_location_link():

    test = 10

    request_link = request.args.get('current_link', '')
    if request_link:
        session['previousLink'] = request_link
        log(log.DEBUG, f'Get current window location link: {request_link}')
        return redirect(url_for("profile.profile"))
    else:
        log(log.ERROR, 'Bad request!', 'No current window location in request!')
        return 'Bad request!'


@profile_blueprint.route("/profile", methods=["GET"])
@login_required
def profile():
    previous_route = session.get('previousLink', '')
    return render_template(
        "profile.html",
        previous_route=previous_route
    )

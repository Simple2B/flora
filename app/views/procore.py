from flask import Blueprint, redirect, session, url_for, current_app
from flask_login import login_required
import requests

from app.procore import ProcoreApi

procore_blueprint = Blueprint("procore", __name__)


@procore_blueprint.route('/procore/get_auth', methods=['GET', 'POST'])
@login_required
def procore_auth():
    api = ProcoreApi()
    session['bool'] = True
    # return redirect(api.make_authorization_url())
    access_token = api.set_access_token
    session["procore_access_token"] = access_token
    return redirect(url_for("bidding.biddings"))


@procore_blueprint.route('/procore/refresh_token', methods=["POST"])
@login_required
def app_refresh_token():
    api = ProcoreApi()
    access_token = session.get('access_token')
    refresh_token = session.get('refresh_token')
    headers = {"Authorization": "Bearer " + access_token}
    data = {
        "client_id": current_app.config['CLIENT_ID'],
        "grant_type": "refresh_token",
        "redirect_uri": current_app.config['REDIRECT_URI'],
        "client_secret": current_app.config['CLIENT_SECRET'],
        "refresh_token": refresh_token
        }
    response = requests.post(current_app.config['BASE_URL']+'/oauth/token', data=data, headers=headers)
    response_json = response.json()
    session['access_token'] = response_json['access_token']
    session['refresh_token'] = response_json['refresh_token']
    session['created_at'] = api.update_date(response_json['created_at'])
    session['expires_at'] = api.update_expire(response_json['created_at'])
    return redirect(url_for('main.index'))


@procore_blueprint.route('/procore/revoke_token', methods=['GET', 'POST'])
@login_required
def app_revoke_token():
    access_token = session.get('access_token')
    data = {
        "client_id": current_app.config['CLIENT_ID'],
        "client_secret": current_app.config['CLIENT_SECRET'],
        "token": access_token
        }
    requests.post(current_app.config['BASE_URL']+'/oauth/token', data=data)
    [session.pop(key) for key in list(session.keys()) if key != '_flashes']
    session['bool'] = False
    return redirect(url_for('main.index'))

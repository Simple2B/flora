from flask import render_template, Blueprint, redirect, url_for, request
from flask_login import login_required

from app.forms import LoginForm, RegistrationForm
from app.models import User


main_blueprint = Blueprint('main', __name__)


@main_blueprint.route('/')
@login_required
def index():
    # return redirect(url_for('main.team'))
    return render_template('index.html')


@main_blueprint.route('/bidding')
@login_required
def bidding():
    return render_template('index.html')


@main_blueprint.route('/team')
@login_required
def team():
    form = RegistrationForm(request.form)
    users = User.query.all()
    return render_template('team.html', form=form, users=users)


@main_blueprint.route('/resources')
@login_required
def resources():
    return render_template('index.html')

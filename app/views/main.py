from flask import render_template, Blueprint, redirect, url_for, request
from app.forms import LoginForm

main_blueprint = Blueprint('main', __name__)


@main_blueprint.route('/')
def index():
    return redirect(url_for('main.team'))


@main_blueprint.route('/bidding')
def bidding():
    return render_template('index.html')


@main_blueprint.route('/team')
def team():
    form = LoginForm(request.form)
    form.user = 'Administrator'
    return render_template('team.html', form=form)


@main_blueprint.route('/resources')
def resources():
    return render_template('index.html')

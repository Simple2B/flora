from flask import render_template, Blueprint, redirect, url_for

main_blueprint = Blueprint('main', __name__)


@main_blueprint.route('/')
def index():
    return redirect(url_for('main.team'))

@main_blueprint.route('/bidding')
def bidding():
    return render_template('index.html')

@main_blueprint.route('/team')
def team():
    return render_template('team.html')

@main_blueprint.route('/resources')
def resources():
    return render_template('index.html')

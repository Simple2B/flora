from flask import render_template, Blueprint, redirect, url_for, request
from flask_login import login_required

from app.forms import RegistrationForm, WorkItemForm
from app.models import User, WorkItem


main_blueprint = Blueprint('main', __name__)


@main_blueprint.route('/')
@login_required
def index():
    # return redirect(url_for('main.team'))
    return render_template('index.html')


@main_blueprint.route('/bidding')
@login_required
def bidding():
    form = WorkItemForm(request.form)
    work_items = WorkItem.query.all()
    test = [
        'test',
        'test',
        'test',
        'test',
        'test',
        'test',
        'test',
        'test'
    ]
    return render_template('bidding.html', form=form, work_items=work_items, test=test)


@main_blueprint.route('/team')
@login_required
def team():
    form = RegistrationForm(request.form)
    users = User.query.all()
    return render_template('team.html', form=form, users=users)


@main_blueprint.route('/resources')
@login_required
def resources():
    return render_template('header.html')


@main_blueprint.route('/work_items')
@login_required
def work_items():
    form = WorkItemForm(request.form)
    work_items = WorkItem.query.all()
    return render_template('work_items.html', form=form, work_items=work_items)


@main_blueprint.route('/exclusions')
@login_required
def exclusions():
    form = WorkItemForm(request.form)
    work_items = WorkItem.query.all()
    return render_template('exclusions.html', form=form, work_items=work_items)


@main_blueprint.route('/clarifications')
@login_required
def clarifications():
    form = WorkItemForm(request.form)
    work_items = WorkItem.query.all()
    return render_template('clarifications.html', form=form, work_items=work_items)


@main_blueprint.route('/header')
@login_required
def header():
    return render_template('header.html')


@main_blueprint.route("/test")
def test():
    return redirect(url_for("main.bidding/#work-item-container"))

from flask import Blueprint, render_template, url_for, redirect, flash, request, session
from flask_login import login_required

from app.models import WorkItem, Bid
from app.forms import NewWorkItemForm, WorkItemCartForm
from app.controllers import add_work_item_validator

work_item_blueprint = Blueprint("work_item", __name__)


@work_item_blueprint.route("/work_item", methods=["POST"])
@login_required
def work_item():
    form = NewWorkItemForm(request.form)
    if form.validate_on_submit():
        if add_work_item_validator(form.code.data):
            work_item = WorkItem(
                name=form.name.data,
                code=form.code.data,
            )
            work_item.save()
            # flash("Registration successful. You are logged in.", "success")
            return redirect(url_for("work_item.work_items"))
        else:
            pass
            # flash("The given data was invalid.", "danger")
            return redirect(url_for("work_item.work_items"))
    elif form.is_submitted():
        flash("The given data was invalid.", "danger")
    return redirect(url_for("work_item.work_items"))


@work_item_blueprint.route("/add_work_item_to_cart", methods=["POST"])
@login_required
def add_work_item_to_cart():
    form = WorkItemCartForm(request.form)
    selected_ids = session.get("SelectedWorkItemsDict", {})
    form.selected_work_items = {
        int(item_id): WorkItem.query.get(item_id) for item_id in selected_ids
    }
    if form.validate_on_submit():
        form.selected_work_items.update(
            {
                str(k): WorkItem.query.get(int(k))
                for k in request.form
                if request.form[k] == "on"
            }
        )
        session["SelectedWorkItemsDict"] = {
            str(item_id): item_id for item_id in form.selected_work_items
        }
        return redirect(url_for("work_item.work_items"))
    elif form.is_submitted():
        pass
        # flash("The given data was invalid.", "danger")
    return redirect(url_for("work_item.work_items"))


@work_item_blueprint.route("/delete_work_item_from_cart/<item_id>", methods=["GET"])
@login_required
def delete_work_item_from_cart(item_id):
    item_id = str(item_id)
    selected_ids = session.get("SelectedWorkItemsDict", {})
    if item_id in selected_ids:
        del selected_ids[item_id]
    session["SelectedWorkItemsDict"] = selected_ids
    return redirect(url_for("work_item.work_items"))


@work_item_blueprint.route(
    "/delete_work_item_from_items/<item_id>", methods=["POST"]
)
@login_required
def delete_work_item_from_items(item_id):
    work_item = WorkItem.query.get(item_id)
    if work_item:
        selected = session.get("SelectedWorkItemsDict", {})
        if str(work_item.id) in selected:
            del selected[str(work_item.id)]
            session['SelectedWorkItemsDict'] = selected
        work_item.delete()
    return redirect(url_for("work_item.work_items"))


@work_item_blueprint.route("/edit_work_item/<item_id>", methods=["POST"])
@login_required
def edit_work_item(item_id):
    item_id = int(item_id)
    form = NewWorkItemForm(request.form)
    if form.validate_on_submit():
        work_item = WorkItem.query.get(item_id)
        if work_item:
            work_item.code = form.code.data
            work_item.name = form.name.data
            work_item.save()
    return redirect(url_for("work_item.work_items"))


@work_item_blueprint.route("/work_items", methods=["GET"])
@login_required
def work_items():
    form = NewWorkItemForm()
    bid = Bid.query.get(1)
    bid.title = 'Test bid'
    work_cart_form = WorkItemCartForm()
    selected_work_item_ids = session.get("SelectedWorkItemsDict", {})
    work_cart_form.selected_work_items = [
        WorkItem.query.get(item_id) for item_id in selected_work_item_ids
    ]
    form.work_items = WorkItem.query.all()
    return render_template(
        "work_items.html",
        form=form,
        bid=bid,
        work_cart_form=work_cart_form,
    )

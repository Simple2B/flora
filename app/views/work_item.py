from flask import Blueprint, render_template, url_for, redirect, flash, request, session
from flask_login import login_required

from app.models import WorkItem, Bid, WorkItemGroup
from app.forms import NewWorkItemForm, WorkItemCartForm, WorkItemGroupForm, WorkItemGroupCartForm
from app.controllers import add_work_item_validator, str_function

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
    form_group = WorkItemGroupCartForm(request.form)
    selected_ids = session.get("SelectedWorkItemsDict", {})
    selected_ids_group = session.get("SelectedWorkItemsGroupDict", {})
    form.selected_work_items = {
        int(item_id): WorkItem.query.get(item_id) for item_id in selected_ids
    }
    selected_work_items_group = {
        int(item_id): WorkItem.query.get(item_id) for item_id in selected_ids_group
    }

    if form.validate_on_submit():

        if form_group.add_submit.data:
            selected_work_items_group.update(
                {
                    str(k): WorkItem.query.get(int(k))
                    for k in request.form
                    if request.form[k] == "on"
                }
            )
            session["SelectedWorkItemsGroupDict"] = {
                str(item_id): item_id for item_id in selected_work_items_group
            }
            return redirect(url_for("work_item.work_items"))

        else:
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
        session["DeletedWorkItem"] = {}
        session["DeletedWorkItem"] = selected_ids[item_id]
        del selected_ids[item_id]
    session["SelectedWorkItemsDict"] = selected_ids
    return redirect(url_for("work_item.work_items"))


@work_item_blueprint.route("/undo_work_item_from_cart/<item_id>", methods=["GET"])
@login_required
def undo_work_item_from_cart(item_id):
    item_id = str(item_id)
    deleted_work_item = session.get("DeletedWorkItem", {})
    selected_ids = session.get("SelectedWorkItemsDict", {})
    if deleted_work_item:
        selected_ids[item_id] = str(item_id)
        session["DeletedWorkItem"] = {}
        return redirect(url_for("work_item.work_items"))
    session["SelectedWorkItemsDict"] = selected_ids
    return redirect(url_for("work_item.work_items"))


#  WorkItemGroup Manipulation
@work_item_blueprint.route("/work_item_group", methods=["POST"])
@login_required
def work_item_group():
    form = WorkItemGroupForm(request.form)
    group_names_all = WorkItemGroup.query.all()
    for i in group_names_all:
        i.delete()
    group_name = WorkItemGroup(
        name=form.name.data
    )
    group_name.save()
    return redirect(url_for("work_item.work_items"))


@work_item_blueprint.route("/delete_work_item_from_group/<item_id>", methods=["GET"])
@login_required
def delete_work_item_from_group(item_id):
    item_id = str(item_id)
    selected_ids = session.get("SelectedWorkItemsGroupDict", {})
    if item_id in selected_ids:
        session["DeletedWorkGroupItem"] = {}
        session["DeletedWorkGroupItem"] = selected_ids[item_id]
        del selected_ids[item_id]
    session["SelectedWorkItemsGroupDict"] = selected_ids
    return redirect(url_for("work_item.work_items"))


@work_item_blueprint.route("/undo_work_item_from_group/<item_id>", methods=["GET"])
@login_required
def undo_work_item_from_group(item_id):
    item_id = str(item_id)
    deleted_work_item_group_id = session.get("DeletedWorkGroupItem", {})
    selected_ids = session.get("SelectedWorkItemsGroupDict", {})
    if deleted_work_item_group_id:
        selected_ids[item_id] = str(item_id)
        session["DeletedWorkGroupItem"] = {}
        return redirect(url_for("work_item.work_items"))
    session["SelectedWorkItemsGroupDict"] = selected_ids
    return redirect(url_for("work_item.work_items"))


#  End WorkItemGroup Manipulation
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
    form_group = WorkItemGroupForm()
    form_group_to_cart = WorkItemGroupCartForm()
    bid = Bid.query.get(1)
    bid.title = 'Test bid'
    work_cart_form = WorkItemCartForm()
    selected_work_item_ids = session.get("SelectedWorkItemsDict", {})
    selected_items_ids_group = session.get("SelectedWorkItemsGroupDict", {})
    deleted_work_item_id = session.get("DeletedWorkItem", {})
    deleted_work_item_group_id = session.get("DeletedWorkGroupItem", {})

    work_cart_form.selected_work_items = [
        WorkItem.query.get(item_id) for item_id in selected_work_item_ids
    ]
    form_group_to_cart.selected_items_group = [
        WorkItem.query.get(item_id) for item_id in selected_items_ids_group
    ]
    form.work_items = WorkItem.query.all()

    group_name = WorkItemGroup.query.all()

    return render_template(
        "work_items.html",
        form=form,
        form_group=form_group,
        form_group_to_cart=form_group_to_cart,
        bid=bid,
        work_cart_form=work_cart_form,
        group_name=group_name,
        deleted_work_item_id=deleted_work_item_id,
        deleted_work_item_group_id=deleted_work_item_group_id,
        str_function=str_function
    )

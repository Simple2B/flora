from flask import Blueprint, render_template, url_for, redirect, flash, request, session
from flask_login import login_required

from app.models import WorkItem, Bid, WorkItemGroup
from app.forms import NewWorkItemForm, WorkItemCartForm, WorkItemGroupForm
from app.controllers import add_work_item_validator, str_function
from app.logger import log

work_item_blueprint = Blueprint("work_item", __name__)


@work_item_blueprint.route("/work_item/<bid_id>", methods=["POST"])
@login_required
def work_item(bid_id):
    form = NewWorkItemForm(request.form)
    if form.validate_on_submit():
        if add_work_item_validator(form.code.data):
            work_item = WorkItem(
                name=form.name.data,
                code=form.code.data,
            )
            work_item.save()
            # flash("Registration successful. You are logged in.", "success")
            return redirect(url_for("work_item.work_items", bid_id=bid_id))
        else:
            pass
            # flash("The given data was invalid.", "danger")
            return redirect(url_for("work_item.work_items", bid_id=bid_id))
    elif form.is_submitted():
        flash("The given data was invalid.", "danger")
    return redirect(url_for("work_item.work_items", bid_id=bid_id))


@work_item_blueprint.route("/add_work_item_to_cart/<bid_id>", methods=["POST"])
@login_required
def add_work_item_to_cart(bid_id):
    form = WorkItemCartForm(request.form)
    if form.validate_on_submit():
        selected_work_items_choices = [
            i for i in request.form
            if (request.form[i] == "on" and not i.startswith("group$"))
        ]

        selected_group_names = [
            i.split('$')[1] for i in request.form
            if (request.form[i] == "on" and i.startswith("group$"))
        ]

        if selected_group_names:
            # Add all selected work items into all selected groups
            groups = session.get("GroupDict", {})
            for group_name in selected_group_names:
                if group_name not in groups:
                    groups[group_name] = []
                for work_item in selected_work_items_choices:
                    groups[group_name] += [work_item]
            session["GroupDict"] = groups
        else:
            # Add all selected work items into global list
            global_work_items = session.get("SelectedWorkItemsDict", {})
            for work_item in selected_work_items_choices:
                global_work_items[work_item] = work_item
            session["SelectedWorkItemsDict"] = global_work_items
    elif form.is_submitted():
        log(log.WARNING, "The given data was invalid")
        # flash("The given data was invalid.", "danger")
    return redirect(url_for("work_item.work_items", bid_id=bid_id))


@work_item_blueprint.route("/delete_work_item_from_cart/<bid_id>/<item_id>", methods=["GET"])
@login_required
def delete_work_item_from_cart(bid_id, item_id):
    item_id = str(item_id)
    selected_ids = session.get("SelectedWorkItemsDict", {})
    if item_id in selected_ids:
        session["DeletedWorkItem"] = selected_ids[item_id]
        del selected_ids[item_id]
        session["SelectedWorkItemsDict"] = selected_ids
    return redirect(url_for("work_item.work_items", bid_id=bid_id))


@work_item_blueprint.route("/undo_work_item_from_cart/<bid_id>/<item_id>", methods=["GET"])
@login_required
def undo_work_item_from_cart(bid_id, item_id):
    item_id = str(item_id)
    deleted_work_item = session.get("DeletedWorkItem", {})
    selected_ids = session.get("SelectedWorkItemsDict", {})
    if deleted_work_item:
        selected_ids[item_id] = str(item_id)
        session["DeletedWorkItem"] = {}
        return redirect(url_for("work_item.work_items", bid_id=bid_id))
    session["SelectedWorkItemsDict"] = selected_ids
    return redirect(url_for("work_item.work_items", bid_id=bid_id))


#  Group Manipulation


@work_item_blueprint.route("/work_item_group/<bid_id>", methods=["POST"])
@login_required
def work_item_group(bid_id):
    form = WorkItemGroupForm(request.form)
    groups = session.get("GroupDict", {})
    group_name = form.name.data
    if group_name not in groups:
        groups[group_name] = []
        session["GroupDict"] = groups
    return redirect(url_for("work_item.work_items", bid_id=bid_id))


@work_item_blueprint.route("/delete_work_item_from_group/<bid_id>/<group_name>/<work_item_id>", methods=["GET"])
@login_required
def delete_work_item_from_group(group_name, work_item_id, bid_id):
    groups = session.get("GroupDict", {})
    if group_name in groups:
        if work_item_id in groups[group_name]:
            groups[group_name].remove(work_item_id)
            session["DeletedWorkGroupItem"] = {group_name: work_item_id}
        session["GroupDict"] = groups
    else:
        log(log.WARNING, "Not found group [%s]!", group_name)
    return redirect(url_for("work_item.work_items", bid_id=bid_id))


@work_item_blueprint.route("/undo_work_item_from_group/<bid_id>/<group_name>/<item_id>", methods=["GET"])
@login_required
def undo_work_item_from_group(group_name, item_id, bid_id):
    item_id = str(item_id)
    selected_ids = session.get("SelectedWorkItemsGroupDict", {})
    deleted_work_item_group_id = session.get("DeletedWorkGroupItem", {})
    groups = session.get("GroupDict", {})
    if deleted_work_item_group_id:
        groups[group_name].append(item_id)
        session["DeletedWorkGroupItem"] = {}
        return redirect(url_for("work_item.work_items", bid_id=bid_id))
    session["SelectedWorkItemsGroupDict"] = selected_ids
    return redirect(url_for("work_item.work_items", bid_id=bid_id))


@work_item_blueprint.route(
    "/delete_group/<bid_id>/<group_name>", methods=["POST"]
)
@login_required
def delete_group(bid_id, group_name):
    if group_name:
        groups = session.get("GroupDict", {})
        if str(group_name) in groups:
            del groups[group_name]
            session['GroupDict'] = groups
    return redirect(url_for("work_item.work_items", bid_id=bid_id))


#  End Group Manipulation


#  WorkItem Manipulation


@work_item_blueprint.route(
    "/delete_work_item/<bid_id>/<item_id>", methods=["POST"]
)
@login_required
def delete_work_item(bid_id, item_id):
    work_item = WorkItem.query.get(item_id)
    if work_item:
        selected = session.get("SelectedWorkItemsDict", {})
        if str(work_item.id) in selected:
            del selected[str(work_item.id)]
            session['SelectedWorkItemsDict'] = selected
        work_item.delete()
    return redirect(url_for("work_item.work_items", bid_id=bid_id))


@work_item_blueprint.route("/edit_work_item/<bid_id>/<item_id>", methods=["POST"])
@login_required
def edit_work_item(bid_id, item_id):
    item_id = int(item_id)
    form = NewWorkItemForm(request.form)
    if form.validate_on_submit():
        work_item = WorkItem.query.get(item_id)
        if work_item:
            work_item.code = form.code.data
            work_item.name = form.name.data
            work_item.save()
    return redirect(url_for("work_item.work_items", bid_id=bid_id))


#  End WorkItem Manipulation


@work_item_blueprint.route("/work_items/<bid_id>", methods=["GET"])
@login_required
def work_items(bid_id):
    form = NewWorkItemForm()
    form_group = WorkItemGroupForm()
    bid_id = bid_id
    work_cart_form = WorkItemCartForm()
    selected_work_item_ids = session.get("SelectedWorkItemsDict", {})
    form.deleted_work_item_id = session.get("DeletedWorkItem", {})
    form_group.deleted_work_item_group_id = session.get("DeletedWorkGroupItem", {})

    work_cart_form.global_work_items = [
        WorkItem.query.get(item_id) for item_id in selected_work_item_ids
    ]

    form.work_items = WorkItem.query.all()

    groups_work_items_ids = session.get("GroupDict", [])
    form_group.groups = {}
    for group in groups_work_items_ids:
        form_group.groups[group] = []
        for work_item_id in groups_work_items_ids[group]:
            form_group.groups[group] += [WorkItem.query.filter(WorkItem.id == int(work_item_id)).first()]

    return render_template(
        "work_items.html",
        form=form,
        form_group=form_group,
        bid_id=bid_id,
        work_cart_form=work_cart_form,
        str_function=str_function,
    )

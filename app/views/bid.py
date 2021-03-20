import io
import os
import json
import datetime

from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    send_file,
    request,
    session,
)
from flask_login import login_required

from app.models import Bid, WorkItemLine, LinkWorkItem, WorkItem, WorkItemGroup

from app.forms import WorkItemLineForm, BidForm

from app.controllers import (
    calculate_subtotal,
    calculate_alternate_total,
    time_update,
    check_bid_tbd,
)

from app.logger import log

import pdfkit


bid_blueprint = Blueprint("bid", __name__)


@bid_blueprint.route("/check_tbd/<int:bid_id>/<tbd_name>", methods=["GET"])
@login_required
def check_tbd(bid_id, tbd_name):
    if tbd_name.startswith("work_item_line_tbd_"):
        line_id = int(tbd_name.strip("work_item_line_tbd_"))
        work_item_line = WorkItemLine.query.get(line_id)
        if work_item_line.tbd:
            return "tbd_work_item_line_on"
        else:
            return "tbd_work_item_line_off"
    elif tbd_name.startswith("alternate_"):
        if tbd_name.endswith("off"):
            return "False"
        return "True"
    bid_tbd = check_bid_tbd(bid_id, tbd_name)
    return f"{bid_tbd}"


@bid_blueprint.route("/save_tbd/<int:bid_id>", methods=["GET"])
@login_required
def save_tbd(bid_id):
    bid = Bid.query.get(bid_id)
    if request.args:
        tbd_name = request.args.get("", None)
        switch = {
            "permit": (lambda: bid.permit_filling_fee),
            "general": (lambda: bid.general_conditions),
            "overhead": (lambda: bid.overhead),
            "insurance": (lambda: bid.insurance_tax),
            "profit": (lambda: bid.profit),
            "bond": (lambda: bid.bond)
        }
        if tbd_name:
            if tbd_name.startswith("work_item_line_tbd_"):
                line_id = int(tbd_name.strip("work_item_line_tbd_"))
                work_item_line = WorkItemLine.query.get(line_id)
                work_item_line.tbd = True
                work_item_line.save()
                log(log.INFO, f"Response: 'work_item_line_tbd_id:{line_id} is True'")
                return f"Work item line: {tbd_name}"
            elif tbd_name.startswith("alternate_"):
                return f"Alternate: {tbd_name}"
            else:
                calculate_subtotal(bid_id, tbd_name=tbd_name)
                log(log.INFO, f"Response is '{tbd_name}'")
        else:
            tbd_name = request.args["false"]
            if tbd_name.startswith("work_item_line_tbd_"):
                line_id = int(tbd_name.strip("work_item_line_tbd_"))
                work_item_line = WorkItemLine.query.get(line_id)
                work_item_line.tbd = False
                work_item_line.save()
                log(log.INFO, f"Response: 'work_item_line_tbd_id:{line_id} is False'")
                return f"Work item line: {tbd_name}"
            elif tbd_name.startswith("alternate_"):
                return f"Alternate: {tbd_name}"
            else:
                calculate_subtotal(bid_id, tbd_name=tbd_name, on_tbd=False)
                log(log.INFO, f"Response: 'tbd_name: {tbd_name} is False'")
                return json.dumps(
                    dict(
                        subtotal=bid.subtotal,
                        grandSubtotal=bid.grand_subtotal,
                        bid_param_name=f'{tbd_name}',
                        bid_param_value=switch[tbd_name](),
                    )
                )
        return json.dumps(
            dict(
                subtotal=bid.subtotal,
                grandSubtotal=bid.grand_subtotal,
                bid_param_name=f'{tbd_name}',
            )
        )
    else:
        session["tbdChoices"] = []
        log(log.ERROR, "No requesr.args")
        return "Error"


@bid_blueprint.route(
    "/add_work_item_line/<bid_id>/<int:link_work_item_id>", methods=["GET"]
)
@login_required
def add_work_item_line(bid_id, link_work_item_id):
    WorkItemLine(link_work_items_id=link_work_item_id).save()
    time_update(bid_id)
    session["saveInCloud"] = True
    session["pageyoffset"] = request.args.get("pageYOffset", "")
    return redirect(url_for("bid.bidding", bid_id=bid_id))


@bid_blueprint.route("/delete_group/<bid_id>/<group_name>", methods=["GET"])
@login_required
def delete_group(bid_id, group_name):
    group = (
        WorkItemGroup.query.filter(WorkItemGroup.bid_id == bid_id)
        .filter(WorkItemGroup.name == group_name)
        .first()
    )
    for link in group.link_work_items:
        for line in link.work_item_lines:
            line.delete()
        link.delete()
    group.delete()
    time_update(bid_id)
    return redirect(url_for("bid.bidding", bid_id=bid_id))


@bid_blueprint.route(
    "/add_group_work_item_line/<bid_id>/<int:group_link_id>", methods=["GET"]
)
@login_required
def add_group_work_item_line(bid_id, group_link_id):
    WorkItemLine(link_work_items_id=group_link_id).save()
    time_update(bid_id)
    return redirect(url_for("bid.bidding", bid_id=bid_id, _anchor="bid_scope_of_work"))


@bid_blueprint.route(
    "/edit_work_item_line/<int:bid_id>/<int:work_item_line_id>", methods=["POST"]
)
@login_required
def edit_work_item_line(bid_id, work_item_line_id):
    form = WorkItemLineForm(request.form)
    if form.validate_on_submit():
        line = WorkItemLine.query.get(work_item_line_id)
        if line:
            if form.tbd.data:
                line.note = form.note.data
                line.description = form.description.data
                line.price = 0.0
                line.unit = form.unit.data
                line.quantity = form.quantity.data
                line.tbd = form.tbd.data
                line.save()
                time_update(bid_id)
            else:
                line.note = form.note.data
                line.description = form.description.data
                line.price = form.price.data
                line.unit = form.unit.data
                line.quantity = form.quantity.data
                line.tbd = form.tbd.data
                line.save()
                time_update(bid_id)
        else:
            log(log.ERROR, "Unknown work_item_line_id: %d", work_item_line_id)

    return redirect(url_for("bid.bidding", bid_id=bid_id, _anchor="bid_scope_of_work"))


@bid_blueprint.route(
    "/delete_link_work_item/<int:bid_id>/<int:link_work_item_id>", methods=["GET"]
)
@login_required
def delete_link_work_item(bid_id, link_work_item_id):
    link = LinkWorkItem.query.get(link_work_item_id)
    if link:
        for line in link.work_item_lines:
            line.delete()
        link.delete()
        time_update(bid_id)
        session["saveInCloud"] = True
    else:
        log(log.ERROR, "Unknown work_item_line_id: %d", link_work_item_id)
    return redirect(url_for("bid.bidding", bid_id=bid_id, _anchor="bid_scope_of_work"))


@bid_blueprint.route(
    "/delete_group_link_work_item/<int:bid_id>/<int:group_link_id>", methods=["GET"]
)
@login_required
def delete_group_link_work_item(bid_id, group_link_id):
    link = LinkWorkItem.query.get(group_link_id)
    if link:
        for line in link.work_item_lines:
            line.delete()
        link.delete()
        time_update(bid_id)
    else:
        log(log.ERROR, "Unknown work_item_line_id: %d", group_link_id)
    return redirect(url_for("bid.bidding", bid_id=bid_id, _anchor="bid_scope_of_work"))


@bid_blueprint.route(
    "/delete_work_item_line/<int:bid_id>/<int:work_item_line_id>", methods=["GET"]
)
@login_required
def delete_work_item_line(bid_id, work_item_line_id):
    line = WorkItemLine.query.get(work_item_line_id)
    session["pageyoffset"] = request.args.get("pageYOffset", "")
    if line:
        line.delete()
        time_update(bid_id)
    else:
        log(log.ERROR, "Unknown work_item_line_id: %d", work_item_line_id)
    return redirect(url_for("bid.bidding", bid_id=bid_id))


@bid_blueprint.route(
    "/delete_group_work_item_line/<int:bid_id>/<int:group_link_id>", methods=["GET"]
)
@login_required
def delete_group_work_item_line(bid_id, group_link_id):
    line = WorkItemLine.query.get(group_link_id)
    session["pageyoffset"] = request.args.get("pageYOffset", "")
    if line:
        line.delete()
        time_update(bid_id)
    else:
        log(log.ERROR, "Unknown work_item_line_id: %d", group_link_id)
    return redirect(url_for("bid.bidding", bid_id=bid_id))


@bid_blueprint.route("/delete_exclusions/<int:bid_id>")
@login_required
def delete_exclusions(bid_id):
    bid = Bid.query.get(bid_id)
    for exclusion_link in bid.exclusion_links:
        exclusion_link.delete()
    session["saveInCloud"] = True
    time_update(bid_id)
    return redirect(url_for("bidding.bidding", bid_id=bid_id, _anchor="bid_exclusion"))


@bid_blueprint.route("/edit_exclusions/<int:bid_id>")
@login_required
def edit_exclusions(bid_id):
    return redirect(url_for("exclusion.exclusions", bid_id=bid_id))


@bid_blueprint.route("/delete_clarifications/<int:bid_id>")
@login_required
def delete_clarifications(bid_id):
    bid = Bid.query.get(bid_id)
    for clarification_link in bid.clarification_links:
        clarification_link.delete()
    session["saveInCloud"] = True
    time_update(bid_id)
    return redirect(url_for("bid.bidding", bid_id=bid_id, _anchor="bid_clarification"))


@bid_blueprint.route("/edit_clarifications/<int:bid_id>")
@login_required
def edit_clarifications(bid_id):
    return redirect(url_for("clarification.clarifications", bid_id=bid_id))


@bid_blueprint.route("/bidding_change_status/<int:bid_id>", methods=["POST"])
@login_required
def bidding_change_status(bid_id):
    BidForm(request.form)
    bid = Bid.query.get(bid_id)
    if request.form.get("bid_status", "") == "Draft":
        bid.status = Bid.Status.b_draft
        bid.save()
    elif request.form.get("bid_status", "") == "Submitted":
        bid.status = Bid.Status.c_submitted
        bid.save()
    else:
        bid.status = Bid.Status.d_archived
        bid.save()
    session["saveInCloud"] = True
    time_update(bid_id)
    return redirect(url_for("bid.bidding", bid_id=bid_id, _anchor="bid_scope_of_work"))


@bid_blueprint.route("/bidding_save_in_cloud/<int:bid_id>", methods=["GET"])
@login_required
def bidding_save_in_cloud(bid_id):
    session["saveInCloud"] = False
    return redirect(url_for("bid.bidding", bid_id=bid_id, _anchor="bid_scope_of_work"))


@bid_blueprint.route("/bidding/<int:bid_id>", methods=["GET"])
@login_required
def bidding(bid_id):
    bid = Bid.query.get(bid_id)
    form_bid = BidForm()
    form = WorkItemLineForm()
    form.pageyoffset = session.get("pageyoffset", "")
    tbd_choices = session.get("tbdChoices", [])
    form_bid.save_in_cloud = False

    if bid.status == Bid.Status.a_new:
        bid.status = Bid.Status.b_draft
    bid.popularity += 1
    bid.save()

    form_bid.global_work_items = (
        LinkWorkItem.query.filter(LinkWorkItem.bid_id == bid_id)
        .filter(LinkWorkItem.work_item_group == None)  # noqa 711
        .all()
    )

    form_bid.groups = WorkItemGroup.query.filter(WorkItemGroup.bid_id == bid_id).all()

    work_items_ides = [
        link_work_item.work_item_id for link_work_item in bid.link_work_items
    ]
    list_work_items = []
    for work_item_id in work_items_ides:
        list_work_items += [WorkItem.query.get(work_item_id)]
    show_exclusions = (", ").join(
        [exclusion_link.exclusion.title for exclusion_link in bid.exclusion_links]
    ) + "."
    show_exclusions = show_exclusions.capitalize()
    show_clarifications = (", ").join(
        [
            clarification_link.clarification.note
            for clarification_link in bid.clarification_links
        ]
    ) + "."
    show_clarifications = show_clarifications.capitalize()
    calculate_subtotal(bid_id, tbd_choices)
    form.calculate_alternate_total = calculate_alternate_total(bid_id)
    session["tbdChoices"] = []
    return render_template(
        "bidding.html",
        bid=bid,
        form=form,
        form_bid=form_bid,
        show_exclusions=show_exclusions,
        show_clarifications=show_clarifications,
        round=round,
    )


# Export document
@bid_blueprint.route("/preview_pdf/<int:bid_id>", methods=["GET"])
@login_required
def preview_pdf(bid_id):
    bid = Bid.query.get(bid_id)
    previous_url = session.get("nextUrl", "/")
    global_work_items = (
        LinkWorkItem.query.filter(LinkWorkItem.bid_id == bid_id)
        .filter(LinkWorkItem.work_item_group == None)  # noqa 711
        .all()
    )
    groups = WorkItemGroup.query.filter(WorkItemGroup.bid_id == bid_id).all()
    preview_pdf_bool = True
    date_today = datetime.datetime.today().strftime("%m/%d/%Y")
    return render_template(
        "export_document.html",
        bid=bid,
        alternate_total=calculate_alternate_total(bid_id),
        date_today=date_today,
        global_work_items=global_work_items,
        groups=groups,
        preview_pdf_bool=preview_pdf_bool,
        previous_url=previous_url,
    )


@bid_blueprint.route("/export/<int:bid_id>", methods=["POST"])
@login_required
def export(bid_id):
    form = BidForm(request.form)
    if form.validate_on_submit():
        bid = Bid.query.get(bid_id)
        global_work_items = (
            LinkWorkItem.query.filter(LinkWorkItem.bid_id == bid_id)
            .filter(LinkWorkItem.work_item_group == None)  # noqa 711
            .all()
        )
        groups = WorkItemGroup.query.filter(WorkItemGroup.bid_id == bid_id).all()
        tbd_choices = [i for i in request.form if request.form[i] == "on"]
        session["tbdChoices"] = tbd_choices
        if form.preview.data:
            session["nextUrl"] = request.form.get("next_url", "/")
            return redirect(url_for("bid.preview_pdf", bid_id=bid_id))
        if form.export_pdf.data or request.form.get("export", False):
            BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            PATH_TO_IMG = os.path.join(BASE_DIR, "static/images/")
            preview_pdf_bool = False
            calculate_subtotal(bid_id, tbd_choices)
            date_today = datetime.datetime.today().strftime("%m/%d/%Y")
            html_content = render_template(
                "export_document.html",
                bid=bid,
                alternate_total=calculate_alternate_total(bid_id),
                date_today=date_today,
                preview_pdf_bool=preview_pdf_bool,
                groups=groups,
                global_work_items=global_work_items,
                path_to_img=PATH_TO_IMG,
            )
            options = {"enable-local-file-access": None}
            pdf_content = pdfkit.from_string(html_content, False, options=options)
            stream = io.BytesIO(pdf_content)

            now = datetime.datetime.now()
            return send_file(
                stream,
                as_attachment=True,
                attachment_filename=f"bidding_{bid_id}_{now.strftime('%Y-%m-%d-%H-%M-%S')}.pdf",
                mimetype="application/pdf",
                cache_timeout=0,
                last_modified=now,
            )

        elif form.export_docx.data:
            preview_pdf_bool = False
            from app.controllers.create_docx import create_docx

            filepath = create_docx(bid_id)
            with open(filepath, "rb") as f:
                stream = io.BytesIO(f.read())
            os.remove(filepath)
            if not stream:
                log(log.ERROR, "archive_or_export() cannot open [%s]", filepath)
                return redirect(url_for("bidding.biddings"))
            now = datetime.datetime.now()
            file_name = f"bidding_#{bid.procore_bid_id}_{now.strftime('%Y-%m-%d-%H-%M-%S')}.docx"
            log(log.DEBUG, "Sending docx file([%s]): [%s]", stream, file_name)
            return send_file(
                stream,
                as_attachment=True,
                attachment_filename=file_name,
                mimetype="application/docx",
                cache_timeout=0,
                last_modified=now,
            )
    else:
        log(log.ERROR, "Form submitted")
        return redirect(url_for("bid.bidding", bid_id=bid_id))


@bid_blueprint.route("/update_due_date/<int:bid_id>/<due_date>", methods=["GET"])
@login_required
def update_due_date(bid_id, due_date):
    bid = Bid.query.get(bid_id)
    bid.due_date = datetime.datetime.strptime(due_date, "%Y-%m-%d")
    bid.save()
    return "OK"


@bid_blueprint.route("/update_revision/<int:bid_id>/<int:revision>", methods=["GET"])
@login_required
def update_revision(bid_id, revision):
    bid = Bid.query.get(bid_id)
    bid.revision = revision
    bid.save()
    return "OK"


@bid_blueprint.route("/project_type/<int:bid_id>/<project_type_name>", methods=["GET"])
@login_required
def project_type(bid_id, project_type_name):
    bid = Bid.query.get(bid_id)
    if project_type_name == "Budget":
        bid.project_type = Bid.ProjectType.a_budget
    else:
        bid.project_type = Bid.ProjectType.b_quote
    bid.save()
    return "OK"


@bid_blueprint.route(
    "/set_percent_value/<int:bid_id>/<parameter_name>/<value>", methods=["GET"]
)
@login_required
def set_percent_value(bid_id, parameter_name, value):
    bid = Bid.query.get(bid_id)
    if parameter_name not in dir(bid):
        log(log.ERROR, "set_percent_value: wrong parameter_name:[%s]", parameter_name)
        return "ERROR"
    bid.__setattr__(parameter_name, value.strip("% "))
    bid.save()
    calculate_subtotal(bid_id=bid_id)
    return "OK"

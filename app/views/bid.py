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

from app.controllers import calculate_subtotal, time_update, check_bid_tbd

from app.logger import log

import pdfkit

# from GrabzIt import GrabzItClient

bid_blueprint = Blueprint("bid", __name__)


@bid_blueprint.route("/check_tbd/<int:bid_id>/<tbd_name>", methods=["GET"])
@login_required
def check_tbd(bid_id, tbd_name):
    if tbd_name.startswith('work_item_line_'):
        work_item_line = WorkItemLine.query.get(int(tbd_name[15:]))
        return f"{work_item_line.price}"
    else:
        bid_tbd = check_bid_tbd(bid_id, tbd_name)
        return f"{bid_tbd}"


@bid_blueprint.route("/save_tbd/<int:bid_id>", methods=["GET"])
@login_required
def save_tbd(bid_id):
    if request.args:
        if request.args.get('', None):
            tbd_name = request.args['']
            calculate_subtotal(bid_id, tbd_name=tbd_name)
            log(log.INFO, f"Response is '{tbd_name}'")
            json_tbd_name = 'tbd: ' + f'{tbd_name}'
            return json.dumps(json_tbd_name)
        else:
            if True:
                tbd_name = request.args['false']
                calculate_subtotal(bid_id, tbd_name=tbd_name, on_tbd=False)
            return json.dumps('tbd:' + 'false')
    else:
        session["tbdChoices"] = []
        log(log.DEBUG, 'No requesr.args')
        return json.dumps('tbd:' + 'false')


@bid_blueprint.route(
    "/add_work_item_line/<bid_id>/<int:link_work_item_id>", methods=["GET"]
)
@login_required
def add_work_item_line(bid_id, link_work_item_id):
    WorkItemLine(link_work_items_id=link_work_item_id).save()
    time_update(bid_id)
    session['saveInCloud'] = True
    return redirect(url_for("bid.bidding", bid_id=bid_id, _anchor="bid_scope_of_work"))


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
    session['saveInCloud'] = True
    return redirect(url_for("bid.bidding", bid_id=bid_id))


@bid_blueprint.route(
    "/add_group_work_item_line/<bid_id>/<int:group_link_id>", methods=["GET"]
)
@login_required
def add_group_work_item_line(bid_id, group_link_id):
    WorkItemLine(link_work_items_id=group_link_id).save()
    time_update(bid_id)
    session['saveInCloud'] = True
    return redirect(url_for("bid.bidding", bid_id=bid_id))


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
                session['saveInCloud'] = True
            else:
                line.note = form.note.data
                line.description = form.description.data
                line.price = form.price.data
                line.unit = form.unit.data
                line.quantity = form.quantity.data
                line.tbd = form.tbd.data
                line.save()
                time_update(bid_id)
                session['saveInCloud'] = True
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
        session['saveInCloud'] = True
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
        session['saveInCloud'] = True
    else:
        log(log.ERROR, "Unknown work_item_line_id: %d", group_link_id)
    return redirect(url_for("bid.bidding", bid_id=bid_id, _anchor="bid_scope_of_work"))


@bid_blueprint.route(
    "/delete_work_item_line/<int:bid_id>/<int:work_item_line_id>", methods=["GET"]
)
@login_required
def delete_work_item_line(bid_id, work_item_line_id):
    line = WorkItemLine.query.get(work_item_line_id)
    if line:
        line.delete()
        time_update(bid_id)
    else:
        log(log.ERROR, "Unknown work_item_line_id: %d", work_item_line_id)
    return redirect(url_for("bid.bidding", bid_id=bid_id, _anchor="bid_scope_of_work"))


@bid_blueprint.route(
    "/delete_group_work_item_line/<int:bid_id>/<int:group_link_id>", methods=["GET"]
)
@login_required
def delete_group_work_item_line(bid_id, group_link_id):
    line = WorkItemLine.query.get(group_link_id)
    if line:
        line.delete()
        time_update(bid_id)
    else:
        log(log.ERROR, "Unknown work_item_line_id: %d", group_link_id)
    return redirect(url_for("bid.bidding", bid_id=bid_id, _anchor="bid_scope_of_work"))


@bid_blueprint.route("/delete_exclusions/<int:bid_id>")
@login_required
def delete_exclusions(bid_id):
    bid = Bid.query.get(bid_id)
    for exclusion_link in bid.exclusion_links:
        exclusion_link.delete()
    session['saveInCloud'] = True
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
    session['saveInCloud'] = True
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
    session['saveInCloud'] = True
    time_update(bid_id)
    return redirect(url_for("bid.bidding", bid_id=bid_id, _anchor="bid_scope_of_work"))


@bid_blueprint.route("/bidding_save_in_cloud/<int:bid_id>", methods=["GET"])
@login_required
def bidding_save_in_cloud(bid_id):
    session['saveInCloud'] = False
    return redirect(url_for("bid.bidding", bid_id=bid_id, _anchor="bid_scope_of_work"))


@bid_blueprint.route("/bidding/<int:bid_id>", methods=["GET"])
@login_required
def bidding(bid_id):
    bid = Bid.query.get(bid_id)
    form_bid = BidForm()
    form = WorkItemLineForm()
    tbd_choices = session.get("tbdChoices", [])
    form_bid.save_in_cloud = session.get('saveInCloud', False)

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
    due_date = datetime.datetime.now().strftime('%Y-%m-%d')
    session["tbdChoices"] = []
    return render_template(
        "bidding.html",
        bid=bid,
        form=form,
        show_exclusions=show_exclusions,
        show_clarifications=show_clarifications,
        form_bid=form_bid,
        due_date=due_date,
        round=round
    )

# Export document


@bid_blueprint.route("/preview_pdf/<int:bid_id>", methods=["GET"])
@login_required
def preview_pdf(bid_id):
    bid = Bid.query.get(bid_id)
    global_work_items = (
        LinkWorkItem.query.filter(LinkWorkItem.bid_id == bid_id)
        .filter(LinkWorkItem.work_item_group == None)  # noqa 711
        .all()
    )
    groups = WorkItemGroup.query.filter(WorkItemGroup.bid_id == bid_id).all()
    preview_pdf_bool = True
    tbd_choices = session.get("tbdChoices", [])
    calculate_subtotal(bid_id, tbd_choices)

    return render_template(
        "export_document.html",
        bid=bid,
        global_work_items=global_work_items,
        groups=groups,
        preview_pdf_bool=preview_pdf_bool,
    )


@bid_blueprint.route("/export_pdf/<int:bid_id>", methods=["POST"])
@login_required
def export_pdf(bid_id):
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
            return redirect(url_for("bid.preview_pdf", bid_id=bid_id))
        if form.export_pdf.data:
            BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            PATH_TO_IMG = os.path.join(BASE_DIR, "static/images/")
            preview_pdf_bool = False
            calculate_subtotal(bid_id, tbd_choices)
            html_content = render_template(
                "export_document.html",
                bid=bid,
                preview_pdf_bool=preview_pdf_bool,
                groups=groups,
                global_work_items=global_work_items,
                path_to_img=PATH_TO_IMG,
            )
            options = {'enable-local-file-access': None}
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
            create_docx()
            # with open()
            # calculate_subtotal(bid_id, tbd_choices)
            # html_content = render_template(
            #     "export_document_docx.html", bid=bid, preview_pdf_bool=preview_pdf_bool
            # )
            # grabzit = GrabzItClient.GrabzItClient(
            #     "NDBhNjEyMmI3MjY5NDExMmEwNzJlOTYzZmY1ZGNiNGM=",
            #     "QD8/MT8/Pz9aP0EIPz8/P096S28/P1M/Bj8/RD8/Pxg=",
            # )
            # grabzit.HTMLToDOCX(html_content)
            # docx_content = grabzit.SaveTo()

            with open('demo.docx', 'rb') as f:
                stream = io.BytesIO(f.read())
            # target_stream = StringIO()
            # document.save(target_stream)
            now = datetime.datetime.now()
            return send_file(
                stream,
                as_attachment=True,
                attachment_filename=f"bidding_{bid_id}_{now.strftime('%Y-%m-%d-%H-%M-%S')}.docx",
                mimetype="application/docx",
                cache_timeout=0,
                last_modified=now,
            )
    else:
        log(log.ERROR, "Form submitted")
        return redirect(url_for("bid.bidding", bid_id=bid_id))

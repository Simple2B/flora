import io
import os
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

from app.controllers import calculate_subtotal

from app.logger import log

import pdfkit
from GrabzIt import GrabzItClient

bid_blueprint = Blueprint("bid", __name__)


@bid_blueprint.route(
    "/add_work_item_line/<bid_id>/<int:link_work_item_id>", methods=["GET"]
)
@login_required
def add_work_item_line(bid_id, link_work_item_id):
    WorkItemLine(link_work_items_id=link_work_item_id).save()
    return redirect(url_for("bid.bidding", bid_id=bid_id, _anchor="bid_scope_of_work"))


@bid_blueprint.route("/delete_group/<bid_id>/<group_name>", methods=["GET"])
@login_required
def delete_group(bid_id, group_name):
    group = WorkItemGroup.query.filter(WorkItemGroup.bid_id == bid_id).filter(
            WorkItemGroup.name == group_name
        ).first()
    for link in group.link_work_items:
        for line in link.work_item_lines:
            line.delete()
        link.delete()
    group.delete()
    return redirect(url_for("bid.bidding", bid_id=bid_id))


@bid_blueprint.route(
    "/add_group_work_item_line/<bid_id>/<int:group_link_id>", methods=["GET"]
)
@login_required
def add_group_work_item_line(bid_id, group_link_id):
    WorkItemLine(link_work_items_id=group_link_id).save()
    return redirect(url_for("bid.bidding", bid_id=bid_id))


@bid_blueprint.route(
    "/edit_work_item_line/<int:bid_id>/<int:work_item_line_id>", methods=["POST"]
)
@login_required
def edit_work_item_line(bid_id, work_item_line_id):
    form = WorkItemLineForm()
    if form.validate_on_submit():
        line = WorkItemLine.query.get(work_item_line_id)
        if line:
            line.note = form.note.data
            line.description = form.description.data
            line.price = form.price.data
            line.unit = form.unit.data
            line.quantity = form.quantity.data
            line.tbd = form.tbd.data
            line.save()
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
    else:
        log(log.ERROR, "Unknown work_item_line_id: %d", group_link_id)
    return redirect(url_for("bid.bidding", bid_id=bid_id, _anchor="bid_scope_of_work"))


@bid_blueprint.route("/delete_exclusions/<int:bid_id>")
@login_required
def delete_exclusions(bid_id):
    bid = Bid.query.get(bid_id)
    for exclusion_link in bid.exclusion_links:
        exclusion_link.delete()
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
    return redirect(url_for("bid.bidding", bid_id=bid_id, _anchor="bid_clarification"))


@bid_blueprint.route("/edit_clarifications/<int:bid_id>")
@login_required
def edit_clarifications(bid_id):
    return redirect(url_for("clarification.clarifications", bid_id=bid_id))


@bid_blueprint.route("/bidding/<int:bid_id>", methods=["GET"])
@login_required
def bidding(bid_id):
    bid = Bid.query.get(bid_id)
    form_bid = BidForm(request.form)
    form = WorkItemLineForm()

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
    calculate_subtotal(bid_id)

    return render_template(
        "bidding.html",
        bid=bid,
        form=form,
        show_exclusions=show_exclusions,
        show_clarifications=show_clarifications,
        form_bid=form_bid,
    )


@bid_blueprint.route("/preview_pdf/<int:bid_id>", methods=["GET"])
@login_required
def preview_pdf(bid_id):
    bid = Bid.query.get(bid_id)
    preview_pdf_bool = True
    tbd_choices = session.get("tbdChoices", [])
    calculate_subtotal(bid_id, tbd_choices)

    return render_template(
        "export_document.html", bid=bid, preview_pdf_bool=preview_pdf_bool
    )


@bid_blueprint.route("/export_pdf/<int:bid_id>", methods=["POST"])
@login_required
def export_pdf(bid_id):
    form = BidForm(request.form)

    if form.validate_on_submit():
        bid = Bid.query.get(bid_id)
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
                path_to_img=PATH_TO_IMG,
            )
            pdf_content = pdfkit.from_string(html_content, False)
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
            calculate_subtotal(bid_id, tbd_choices)
            html_content = render_template(
                "export_document_docx.html", bid=bid, preview_pdf_bool=preview_pdf_bool
            )
            grabzit = GrabzItClient.GrabzItClient(
                "NDBhNjEyMmI3MjY5NDExMmEwNzJlOTYzZmY1ZGNiNGM=",
                "QD8/MT8/Pz9aP0EIPz8/P096S28/P1M/Bj8/RD8/Pxg=",
            )
            grabzit.HTMLToDOCX(html_content)
            docx_content = grabzit.SaveTo()
            stream = io.BytesIO(docx_content)
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

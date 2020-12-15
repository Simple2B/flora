import os
import io
import datetime

from flask import render_template, send_file

from .price import calculate_subtotal

from app.models import Bid, LinkWorkItem, WorkItemGroup
import pdfkit


def upload_pdf_file(bid_id):
    bid = Bid.query.get(bid_id)
    global_work_items = (
        LinkWorkItem.query.filter(LinkWorkItem.bid_id == bid_id)
        .filter(LinkWorkItem.work_item_group == None)  # noqa 711
        .all()
    )
    groups = WorkItemGroup.query.filter(WorkItemGroup.bid_id == bid_id).all()
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    PATH_TO_IMG = os.path.join(BASE_DIR, "static/images/")
    preview_pdf_bool = False
    calculate_subtotal(bid_id)
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

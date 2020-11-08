from flask_wtf import FlaskForm
from wtforms import SubmitField


class BidForm(FlaskForm):
    """Common form for processing all requests with bid
    """
    preview = SubmitField('Preview')  # selected "Export Preview"
    export_pdf = SubmitField('Export to PDF')  # pressed "export to PDF"
    export_docx = SubmitField('Export to DOCX')  # pressed "export to DOCX"

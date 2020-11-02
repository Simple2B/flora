from flask_wtf import FlaskForm
from wtforms import SubmitField


class BidForm(FlaskForm):
    preview = SubmitField('Preview')
    export_pdf = SubmitField('Export to PDF')
    export_docx = SubmitField('Export to DOCX')

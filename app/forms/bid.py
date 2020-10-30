from flask_wtf import FlaskForm
from wtforms import SubmitField


class BidForm(FlaskForm):
    preview = SubmitField('Preview')
    export = SubmitField('Export')

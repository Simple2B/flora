from flask_wtf import FlaskForm
from wtforms import SubmitField


class WorkItemLineForm(FlaskForm):
    submit = SubmitField('Add Line')

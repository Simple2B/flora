from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length


class NewWorkItemForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(2, 30)])
    code = StringField('Code', validators=[DataRequired(), Length(2, 30)])
    submit = SubmitField('Add new work item')


class WorkItemCartForm(FlaskForm):
    submit = SubmitField('Add to bidding')

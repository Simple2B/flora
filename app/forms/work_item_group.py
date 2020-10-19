from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length


class WorkItemGroupForm(FlaskForm):
    name = StringField('name', validators=[DataRequired(), Length(2, 30)])
    submit = SubmitField('Create Group')

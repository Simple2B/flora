from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, FloatField, BooleanField
from wtforms.validators import DataRequired, InputRequired


class WorkItemLineForm(FlaskForm):
    submit = SubmitField('Save')
    note = TextAreaField('Note')
    description = TextAreaField('Description')
    price = FloatField('Price', validators=[InputRequired()])
    unit = StringField('Unit')
    quantity = FloatField('Quantity', validators=[DataRequired()])
    tbd = BooleanField('TDB')

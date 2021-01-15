from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    SubmitField,
    FloatField,
    BooleanField
)
from wtforms.validators import DataRequired, Length, NumberRange, InputRequired


class AlternateForm(FlaskForm):
    name = StringField("Alternate Item", validators=[DataRequired(), Length(1, 128)])
    tbd = BooleanField("TDB")
    description = StringField("Description", default="")
    quantity = FloatField("Quantity", default='1.0', validators=[InputRequired(), NumberRange(min=0)])
    unit = StringField("Unit", default='LS', validators=[DataRequired()])
    price = FloatField("Price", default='0.0', validators=[DataRequired()])
    save_submit = SubmitField("Save")

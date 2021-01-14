from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    SubmitField,
    TextField,
    FloatField,
    BooleanField
)
from wtforms.validators import DataRequired, Length


class AlternateForm(FlaskForm):
    name = StringField("Alternate Item", validators=[DataRequired(), Length(1, 128)])
    tbd = BooleanField("TDB")
    description = TextField("Description")
    quantity = FloatField("Quantity", default='1', validators=[DataRequired()])
    unit = StringField("Unit", default='LS', validators=[DataRequired()])
    price = FloatField("Price", default='0.0', validators=[DataRequired()])
    save_submit = SubmitField("Save")

from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    SubmitField,
    TextField,
    FloatField,
    BooleanField,
)
from wtforms.validators import DataRequired, Length


class AlternateForm(FlaskForm):
    name = StringField("Alternate Item", validators=[DataRequired(), Length(1, 128)])
    description = TextField("Description", validators=[DataRequired()])
    price = FloatField("Price", validators=[DataRequired()])
    unit = StringField("Unit")
    quantity = FloatField("Quantity", validators=[DataRequired()])
    tbd = BooleanField("TDB")
    save_submit = SubmitField("Save")

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length


class ClarificationForm(FlaskForm):
    note = StringField('Note', validators=[DataRequired(), Length(2, 64)])
    description = StringField('Description', validators=[DataRequired()])
    submit = SubmitField('Add new clarification')
    save_submit = SubmitField('Save')


class ClarificationCartForm(FlaskForm):
    submit = SubmitField('Add to cart')

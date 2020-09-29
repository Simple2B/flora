from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextField
from wtforms.validators import DataRequired, Length


class ClarificationForm(FlaskForm):
    note = StringField('Note', validators=[DataRequired(), Length(2, 64)])
    description = TextField('Description', validators=[DataRequired()])
    submit = SubmitField('Add new clarification')
    save_submit = SubmitField('Add new clarification')


class ClarificationCartForm(FlaskForm):
    submit = SubmitField('Add to cart')

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextField
from wtforms.validators import DataRequired, Length


class ExclusionForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(2, 64)])
    description = TextField('Description', validators=[DataRequired()])
    submit = SubmitField('Add new exclusion')
    save_submit = SubmitField('Save')


class ExclusionCartForm(FlaskForm):
    submit = SubmitField('Add to bidding')

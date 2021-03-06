from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length


class ExclusionForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(2, 64)])
    submit = SubmitField('Add new exclusion')
    save_submit = SubmitField('Save')


class ExclusionCartForm(FlaskForm):
    submit = SubmitField('Add to cart')

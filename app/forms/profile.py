from flask import request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, PasswordField, ValidationError
from wtforms.validators import DataRequired, Email, Length, EqualTo
from flask_login import current_user


class ProfileForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(2, 30)])
    email = StringField("Email Address", validators=[DataRequired(), Email()])
    position = StringField("Position", validators=[DataRequired()])
    phone = IntegerField("Phone", validators=[DataRequired()])

    password = PasswordField("Password")
    password_confirmation = PasswordField(
        "Confirm Password",
        validators=[
            EqualTo("password", message="Password do not match."),
        ],
    )

    def validate_password(form, field):
        length_password = len(field.data)
        if length_password > 0:
            if length_password > 30 or length_password < 6:
                raise ValidationError("Password field must be between 6 and 30 characters long.")

    submit = SubmitField('Save changes')

    def __init__(self, *args, **kvarg):
        if current_user:
            super().__init__()
            if request and request.method == 'GET':
                self.username.data = current_user.username
                self.email.data = current_user.email
                self.position.data = current_user.position
                self.phone.data = current_user.phone

from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    PasswordField,
    SubmitField,
    ValidationError,
)
from wtforms.validators import DataRequired, Email, Length, EqualTo

from app.models import User


class LoginForm(FlaskForm):
    user_id = StringField("Username or Email", [DataRequired()])
    password = PasswordField("Password", [DataRequired()])
    submit = SubmitField("Login")


class RegistrationForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(2, 30)])
    email = StringField("Email Address", validators=[DataRequired(), Email()])
    position = StringField("Position", validators=[DataRequired()])
    phone = StringField("Phone", validators=[DataRequired()])
    user_type = StringField("User type", validators=[DataRequired()])

    password = PasswordField("Password", validators=[DataRequired(), Length(6, 30)])
    password_confirmation = PasswordField(
        "Confirm Password",
        validators=[
            DataRequired(),
            EqualTo("password", message="Password do not match."),
        ],
    )
    submit = SubmitField("Add new user")

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first() is not None:
            raise ValidationError("This username is taken.")

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first() is not None:
            raise ValidationError("This email is already registered.")


class EditUserForm(RegistrationForm):
    def validate_username(self, field):
        # do not validate
        pass

    def validate_email(self, field):
        # do not validate
        pass

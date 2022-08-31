from flask_wtf import FlaskForm
from wtforms.validators import InputRequired, Length
from wtforms import StringField, PasswordField

class UserForm(FlaskForm):
    """Form to register new user"""

    username = StringField("Username", validators=[InputRequired(message='Enter Username.'), Length(min=1, max=20, message='Length between 1-20 characters.')])
    password = PasswordField("Password", validators=[InputRequired(message='Enter password.'), Length(min=6, max=30, message='Length between 6-30 characters.')])
    email = StringField("Email Address", validators=[InputRequired(message='Enter email.'), Length(min=6, max=50, message='Length between 6-50 characters.')])
    first_name = StringField("First name", validators=[InputRequired(message='Enter first name.'), Length(min=1, max=30, message='Length between 1-30 characters.')])
    last_name = StringField("Last name", validators=[InputRequired(message='Enter last name.'), Length(min=1, max=30, message='Length between 1-30 characters.')])

class LoginForm(FlaskForm):
    """Form to login existing user."""

    username = StringField("Username", validators=[InputRequired(message='Enter Username.'), Length(min=1, max=20, message='Length between 1-20 characters.')])
    password = PasswordField("Password", validators=[InputRequired(message='Enter password.'), Length(min=6, max=30, message='Length between 6-30 characters.')])

class FeedbackForm(FlaskForm):
    """Form to add feedback for a logged in User."""

    title = StringField("Title", validators=[InputRequired(message='Enter a title.'), Length(min=1, max=100, message='Length between 1-100 characters.')])
    content = StringField("Content", validators=[InputRequired(message='Enter content.'), Length(min=1, max=255, message='Length betweeen 1-255 characters.')])
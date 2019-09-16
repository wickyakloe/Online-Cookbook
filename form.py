from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired


# Flask-WTForm
class LoginForm(FlaskForm):
    """Login form to access the locked pages"""

    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])


class RegisterForm(LoginForm):
    """Register form to create a account"""

    display_name = StringField('display_name', validators=[DataRequired()])
    country = StringField('country', validators=[DataRequired()])

from werkzeug.security import check_password_hash


# User model for Flask-Login
class User():
    """
    This is required to make Flask-Login work
    see: https://flask-login.readthedocs.io/en/latest/#your-user-class
    """
    def __init__(self, username, display_name):
        self.username = username
        self.display_name = display_name

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.username

    @staticmethod
    def validate_login(password_hash, password):
        return check_password_hash(password_hash, password)

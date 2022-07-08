from flask_login import LoginManager, UserMixin
from werkzeug.security import check_password_hash
from flask_wtf import FlaskForm

from .__init__ import app, login_manager


from werkzeug.security import generate_password_hash
# ...
USERS = [
    {
        "id": 1,
        "name": 'tom',
        "password": generate_password_hash('123')
    }
]

import uuid
def create_user(user_name, password):
    user = {
        "name": user_name,
        "password": generate_password_hash(password),
        "id": uuid.uuid4()
    }
    USERS.append(user)

def get_user(user_name):
    for user in USERS:
        if user.get("name") == user_name:
            return user
    return None

class User(UserMixin):
    def __init__(self, user):
        self.username = user.get("name")
        self.password_hash = user.get("password")
        self.id = user.get("id")

    def verify_password(self, password):
        if self.password_hash is None:
            return False
        return check_password_hash(self.password_hash, password)

    def get_id(self):
        return self.id

    @staticmethod
    def get(user_id):
        if not user_id:
            return None
        for user in USERS:
            if user.get('id') == user_id:
                return User(user)
        return None





@login_manager.user_loader  
def load_user(user_id):
    return User.get(user_id)


from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, EqualTo

class LoginForm(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
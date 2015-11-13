import datetime
from flask import url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask.ext.login import UserMixin
from . import db, login_manager

Permission = ('admin', 'writer', 'normal')


class User(UserMixin, db.Document):
    email = db.EmailField(required=True, unique=True)
    username = db.StringField(max_length=20, required=True, unique=True)
    password_hash = db.StringField(max_length=128, required=True)
    user_type = db.StringField(choices=Permission, default='normal')

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)


@login_manager.user_loader
def user_load(user_id):
    return User.objects(id=user_id).first()


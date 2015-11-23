# coding: utf-8
import datetime
from flask import url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask.ext.login import UserMixin
from . import db, login_manager


class User(UserMixin, db.Document):
    """
    用户文档集
    """
    name = db.StringField(max_length=25, required=True, unique=True)
    password_hash = db.StringField(max_length=128, required=True)
    email = db.EmailField(required=True, unique=True)
    url = db.StringField(max_length=30)
    screenName = db.StringField(max_length=25)
    group = db.StringField(default='normal')

    meta = {
        'indexes': [
            'name',
            'email'
        ]
    }

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


class Post(db.DynamicDocument):
    created = db.DateTimeField(default=datetime.datetime.now, required=True)
    title = db.StringField(max_length=255, required=True)
    slug = db.StringField(max_length=255, required=True)
    text = db.StringField()
    status = db.BooleanField(default=False)
    tags = db.ListField(db.StringField())
    author = db.StringField(default="")
    category = db.StringField(default="")


    meta = {
        'indexes': [
            'slug',
            'author',
            'status',
            'category'
        ],
        'ordering': [
            '-created'
        ]
    }


class Page(db.DynamicDocument):
    created = db.DateTimeField(default=datetime.datetime.now, required=True)
    title = db.StringField(max_length=255, required=True)
    slug = db.StringField(max_length=255, required=True)
    text = db.StringField(default="")
    status = db.BooleanField(default=False)
    author = db.StringField(default="")
    category = db.StringField(default="")

    meta = {
        'indexes': [
            'slug',
            'author',
            'status'
        ]
    }


class Category(db.Document):
    name = db.StringField(required=True)
    parent = db.StringField(required=True, default="")

    meta = {
        'indexes':[
            'name'
        ]
    }



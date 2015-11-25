# coding: utf-8
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask.ext.login import UserMixin
from . import db, login_manager


class User(UserMixin, db.Document):
    """
    用户文档集
    """
    name = db.StringField(max_length=25, required=True, unique=True)
    password_hash = db.StringField(max_length=128, required=True)
    email = db.EmailField(required=True, unique=True, default="")
    url = db.StringField(max_length=30, default="")
    screenName = db.StringField(max_length=25, default="")
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
    created = db.DateTimeField(default=datetime.now, required=True)
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
    created = db.DateTimeField(default=datetime.now, required=True)
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


class ChildrenCategory(db.EmbeddedDocument):
    name = db.StringField(required=True)


class Category(db.Document):
    parent = db.StringField(required=True, default="")
    name = db.StringField(required=True, unique=True)
    slug = db.StringField()
    description = db.StringField()
    children = db.ListField(db.EmbeddedDocumentField(ChildrenCategory))

    meta = {
        'indexes': [
            'name'
        ]
    }

# coding: utf-8
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask.ext.login import UserMixin
from . import db, login_manager


class Site(db.Document):
    site_title = db.StringField()
    site_description = db.StringField()
    site_url = db.StringField()


class User(UserMixin, db.Document):
    """
    admin test count
    User(name="admin", password="admin", email="admin@admin.com", url="admin.admin",screenName="admin", group="administrator").save()
    """
    name = db.StringField(max_length=25, required=True, unique=True)
    password = db.StringField()
    password_hash = db.StringField(max_length=128, required=True)
    email = db.EmailField(required=True, unique=True, default="")
    url = db.StringField(max_length=30, default="")
    screenName = db.StringField(max_length=25, default="")
    group = db.StringField(default='subscriber', choices=["administrator", "editor", "subscriber"])

    meta = {
        'indexes': [
            'name',
            'email'
        ]
    }

    def clean(self):
        self.password_hash = generate_password_hash(self.password)
        self.password = None

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

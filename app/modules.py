# coding: utf-8
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask.ext.login import UserMixin
from mongoengine import *
from . import db, login_manager


class User(UserMixin, db.Document):
    """
    admin test count
    User(username="admin", password="admin", email="admin@admin.com", url="admin.admin",screenName="admin", group="administrator").save()
    """
    username = db.StringField(max_length=25, required=True, unique=True)
    password = db.StringField()
    password_hash = db.StringField(max_length=128, required=True)
    email = db.EmailField(required=True, unique=True, default="")
    url = db.StringField(max_length=30, default="")
    screenName = db.StringField(max_length=25, default="")
    group = db.StringField(default='subscriber', choices=["administrator", "editor", "subscriber"])

    meta = {
        'indexes': [
            'username',
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


class Comment(db.EmbeddedDocument):
    """
    comment1 = Comment(author_name="lleohao", content="good post")
    """
    author_name = db.StringField(required=True)
    author_email = db.StringField()
    author_url = db.StringField()
    created = db.DateTimeField(default=datetime.now, required=True)
    content = db.StringField(required=True)


class Category(db.Document):
    """
    Category(name="默认分类", slug="normal", description="这是系统默认的分类")
    """
    name = db.StringField(required=True, unique=True)
    slug = db.StringField()
    description = db.StringField()

    meta = {
        'indexes': [
            'name'
        ]
    }


class Content(db.DynamicDocument):
    """
    post = Content(title="test post", slug="test", status=True, type="post")
    """
    created = db.DateTimeField(default=datetime.now, required=True)
    title = db.StringField(max_length=255, required=True)
    slug = db.StringField(max_length=255, required=True)
    category = db.ReferenceField(Category)
    tags = db.ListField(db.StringField())
    text = db.StringField()
    author = db.StringField(default="")
    status = db.BooleanField(default=False)
    type = db.StringField(choices=["post", "page"])

    comments = db.ListField(db.EmbeddedDocumentField(Comment))

    meta = {
        'indexes': [
            'author',
            'status',
            'category',
            'type'
        ],
        'ordering': [
            '-created'
        ]
    }


class Options(db.Document):
    """
    Options(site_url="lleohao.com", site_title="Lleohao's Blog", site_keyword="blog,python")
    """
    site_url = db.StringField()
    site_title = db.StringField()
    site_keyword = db.StringField()
    site_description = db.StringField()

    comment_index = db.IntField(default=0, required=True)
    new_comment = db.ListField(db.ReferenceField(Content))

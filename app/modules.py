# coding: utf-8
import uuid
from datetime import datetime

from flask import Markup
from flask.ext.login import UserMixin
from markdown import markdown
from werkzeug.security import generate_password_hash, check_password_hash

from . import db, login_manager


def create_only_slug(form):
    if form.slug.data == "":
        slug = str(datetime.now())[0:10] + "-" + str(uuid.uuid4())[0:4]
    else:
        slug = form.slug.data
    return slug


# 用户数据模型
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

    def set_and_save(self, form):
        self.username = form.username.data
        self.email = form.email.data
        self.password = form.password.data
        self.url = form.url.data
        self.screenName = form.screenName.data
        self.group = form.group.data
        self.save()


@login_manager.user_loader
def user_load(user_id):
    return User.objects(id=user_id).first()


# 评论数据模型
class Comment(db.EmbeddedDocument):
    """
    comment1 = Comment(author_name="lleohao", content="good post")
    """
    author_name = db.StringField(required=True)
    author_email = db.StringField()
    author_url = db.StringField()
    created = db.DateTimeField(default=datetime.now, required=True)
    content = db.StringField(required=True)


# 分类数据模型
class Category(db.Document):
    """
    Category(name="默认分类", slug="normal", description="这是系统默认的分类")
    Category(name="Python", slug="python", description="").save()
    """
    name = db.StringField(required=True, unique=True)
    slug = db.StringField(required=True, unique=True)
    description = db.StringField()

    meta = {
        'indexes': [
            'name',
            '$name',
            '#name'
        ]
    }

    def set_val(self, form):
        self.name = form.name.data
        self.slug = form.slug.data
        self.description = form.description.data


# 内容数据模型
class Content(db.DynamicDocument):
    """
    post = Content(title="test post", slug="test", status=True, type="post")
    """
    created = db.DateTimeField(default=datetime.now, required=True)
    title = db.StringField(max_length=255, required=True)
    slug = db.StringField(max_length=255, required=True, unique=True)
    category = db.ReferenceField(Category)
    tags = db.ListField(db.StringField())
    md_text = db.StringField()
    html_text = db.StringField()
    description = db.StringField()
    status = db.BooleanField(default=False)
    type = db.StringField(choices=["post", "page"])
    comments = db.ListField(db.EmbeddedDocumentField(Comment))
    meta = {
        'indexes': [
            'status',
            'category',
            'type'
        ],
        'ordering': [
            '-created'
        ]
    }

    def set_val(self, form, type):
        self.created = datetime.now()
        self.title = form.title.data
        self.slug = create_only_slug(form)
        self.md_text = form.content.data
        if type == 'post':
            if form.tags.data is not "":
                self.tags = form.tags.data.split(",")
            else:
                self.tags = []
            self.category = Category.objects(slug=form.category.data).first()
        else:
            self.tags = None
            self.category = None


    def clean(self):
        op = Options.objects().first()
        self.html_text = Markup(markdown(self.md_text))
        self.description = op.site_title + " - " + op.site_description + " - " + self.md_text[0:150]


# 网站设置属性数据模型
class Options(db.Document):
    url = db.StringField(required=True)
    title = db.StringField(required=True)
    keyword = db.StringField()
    description = db.StringField()
    duoshuo_name = db.StringField(default="")

    # 做为自增长 id 用
    # 暂不需要
    comment_index = db.IntField(default=0, required=True)
    content_index = db.IntField(default=0)

    def set_and_save(self, form):
        self.url = form.url.data
        self.title = form.title.data
        self.keyword = form.keyword.data
        self.description = form.description.data
        self.duoshuo_name = form.duoshuo_name.data
        self.save()

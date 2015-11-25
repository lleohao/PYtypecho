# -*- coding:utf-8 -*-
import random, string
from datetime import date
from flask.ext.wtf import Form
from flask.ext.wtf.html5 import EmailField
from wtforms import StringField, SubmitField, PasswordField, BooleanField, TextAreaField, SelectField
from wtforms.validators import InputRequired, Length, Email, Regexp, EqualTo


class postForm(Form):
    title = StringField(u"标题", validators=[InputRequired()])
    slug = StringField(u"Slug")
    tags = StringField(u"标签")
    category = StringField(u"分类")


class pageForm(Form):
    title = StringField(u"标题", validators=[InputRequired()])
    slug = StringField(u"Slug")


class categoryForm(Form):
    choices = [('', u'不选择')]

    name = StringField(u"分类名称*", validators=[InputRequired()])
    slug = StringField(u"分类缩略名")
    parent = SelectField(u'父级分类', choices=choices, default='')
    description = TextAreaField(u"分类描述")

    def setChoices(self, choices, default=''):
        self.parent.choices = choices
        self.parent.default = default


class userForm(Form):
    choices = [
        ("subscriber", u"关注者"),
        ("editor", u"编辑"),
        ("administrator", u"管理员"),

    ]

    username = StringField(u"用户名*")
    email = EmailField(u"电子邮件*")
    screenName = StringField(u"用户昵称")
    password = PasswordField(u"用户密码*", validators=[EqualTo("password2", message="密码不相同")])
    password2 = PasswordField(u"用户密码确认*")
    url = StringField(u"用户主页")
    group = SelectField(u"用户组", choices=choices, default=["subscriber"])

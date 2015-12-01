# -*- coding:utf-8 -*-
import random, string
from datetime import date
from flask.ext.wtf import Form
from flask.ext.wtf.html5 import EmailField, URLField
from wtforms import StringField, SubmitField, PasswordField, BooleanField, TextAreaField, SelectMultipleField, \
    SelectField, HiddenField
from wtforms.validators import InputRequired, Length, Email, Regexp, EqualTo


class ContentForm(Form):
    content_id = HiddenField()
    title = StringField(u"标题", validators=[InputRequired()])
    slug = StringField(u"Slug")
    tags = StringField(u"标签")
    category = SelectField(u"选择分类", choices=[("normal",u"默认分类")], default="normal")


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


class OptionGeneralForm(Form):
    title = StringField(u"网站标题", description=u"站点的名称将显示在网页的标题处.")
    url = URLField(u"网站地址", description=u"站点地址主要用于生成内容的永久链接.")
    description = StringField(u"网站描述", description=u"站点描述将显示在网页代码的头部.")
    keyword = StringField(u"关键字", description=u"请以半角逗号\",\"分割多个关键字.")
    submit = SubmitField(u"保存设置")

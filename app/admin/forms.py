# -*- coding:utf-8 -*-
from datetime import date
from flask.ext.wtf import Form
from wtforms import StringField, SubmitField, PasswordField, BooleanField, ValidationError
from wtforms.validators import InputRequired, Length, Email, Regexp, EqualTo


class addPostForm(Form):
    title = StringField(u"标题", validators=[InputRequired()])
    slug = StringField(u"Slug", default=date.today())
    submit = SubmitField(u"发布文章")
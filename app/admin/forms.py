# -*- coding:utf-8 -*-
import random, string
from datetime import date
from flask.ext.wtf import Form
from wtforms import StringField, SubmitField, PasswordField, BooleanField, TextAreaField
from wtforms.validators import InputRequired, Length, Email, Regexp, EqualTo


class postForm(Form):
    title = StringField(u"标题", validators=[InputRequired()])
    slug = StringField(u"Slug")
    tags = StringField(u"标签")


class pageForm(Form):
    title = StringField(u"标题", validators=[InputRequired()])
    slug = StringField(u"Slug")
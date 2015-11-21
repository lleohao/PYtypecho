# -*- coding:utf-8 -*-
from flask.ext.wtf import Form
from wtforms import StringField, SubmitField, PasswordField, BooleanField, ValidationError
from wtforms.validators import InputRequired, Length, Email, Regexp, EqualTo
from ..modules import User


class loginForm(Form):
    username = StringField(u"用户名", validators=[InputRequired()])
    password = PasswordField(u"密码", validators=[InputRequired()])
    remember_me = BooleanField(u"下次自动登录")
    submit = SubmitField(u"登录")

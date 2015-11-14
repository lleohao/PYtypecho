# -*- coding:utf-8 -*-
from flask.ext.wtf import Form
from wtforms import StringField, SubmitField, PasswordField, BooleanField, ValidationError
from wtforms.validators import InputRequired, Length, Email, Regexp, EqualTo
from ..modules import Comment, Post
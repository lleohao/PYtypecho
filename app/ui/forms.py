# coding: utf-8
from flask.ext.wtf import Form
from wtforms import Label
from wtforms.fields import StringField, SelectField, SubmitField, PasswordField, RadioField, \
    DateField, DecimalField, SelectMultipleField


class userForm(Form):
    name = StringField(u'用户名')
    age = DateField(u'年龄', format='%Y-%M-%D')
    long = DecimalField(u'25', places=2, rounding=None)
    sex = RadioField(u'性别', choices=[('man', u'男'), ('women', u'女')], default='women')
    language = SelectMultipleField(u'Programming Language',
                                   choices=[('cpp', 'C++'), ('py', 'Python'), ('text', 'Plain Text')])

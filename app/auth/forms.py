# -*- coding:utf-8 -*-
from flask.ext.wtf import Form
from wtforms import StringField, SubmitField, PasswordField, BooleanField, ValidationError
from wtforms.validators import InputRequired, Length, Email, Regexp, EqualTo
from ..modules import User


class loginForm(Form):
    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])
    remember_me = BooleanField("Keep me logged in")
    submit = SubmitField("Submit")


class registerForm(Form):
    email = StringField("Email", validators=[InputRequired(), Length(1, 64),
                                             Email()])
    username = StringField("Username", validators=[
        InputRequired(), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                               'Usernames must have only letters, '
                                               'numbers, dots or underscores')])
    password = PasswordField('Password', validators=[
        InputRequired(), EqualTo('password2', message='Passwords must match.')])
    password2 = PasswordField('Confirm password', validators=[InputRequired()])
    submit = SubmitField("Register")

    def vilidate_email(self, field):
        if User.objects(email=field.data).first():
            ValidationError('Email already registered.')

    def validate_username(self, field):
        if User.objects(username=field.data).first():
            raise ValidationError('Username already in use.')

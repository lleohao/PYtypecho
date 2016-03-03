# coding: utf-8
from flask import render_template, redirect, url_for, flash, session
from flask.ext.login import login_required, login_user, logout_user, current_user, login_fresh

from . import auth
from .forms import LoginForm
from ..modules import User


@auth.route("/")
@auth.route("/login", methods=["GET", "POST"])
def login():
    # 判断用户是否登录
    if login_fresh():
        return redirect(url_for("admin.main"))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.objects(username=form.username.data).first()
        if user is not None and user.verify_password(form.password.data):
            session["username"] = user.username
            login_user(user, form.remember_me.data)
            return redirect(url_for("admin.main"))
        flash(u"用户名或密码错误", 'warning')
    return render_template("login.html", form=form, current_user=current_user)


@auth.route("/logout")
@login_required
def logout():
    session["username"] = None
    logout_user()
    flash(u"您已经退出登录", 'success')
    return redirect(url_for("auth.login"))

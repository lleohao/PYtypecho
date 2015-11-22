# coding: utf-8
from flask import render_template, redirect, request, url_for, flash
from flask.ext.login import login_required, login_user, logout_user, session
from . import auth
from ..modules import User
from .forms import loginForm


@auth.route("/login", methods=["GET", "POST"])
def login():
    form = loginForm()
    if form.validate_on_submit():
        user = User.objects(name=form.username.data).first()
        if user is not None and user.verify_password(form.password.data):
            session["username"] = user.name
            login_user(user, form.remember_me.data)
            return redirect(request.args.get('next') or url_for("admin.main"))
        flash(u"用户名或密码错误", 'warning')
    return render_template("auth/login.html", form=form)


@auth.route("/logout")
@login_required
def logout():
    form = loginForm()
    logout_user()
    session["username"] = None
    flash(u"您已经退出登录", 'success')
    return render_template("auth/login.html", form=form)
# coding: utf-8
from flask import render_template, redirect, request, url_for, flash
from flask.ext.login import login_required, login_user, logout_user, session
from . import auth
from ..modules import User
from .forms import loginForm, registerForm


@auth.route("/login", methods=["GET", "POST"])
def login():
    form = loginForm()
    if form.validate_on_submit():
        user = User.objects(username=form.username.data).first()
        if user is not None and user.verify_password(form.password.data):
            session["username"] = user.username
            login_user(user, form.remember_me.data)
            return redirect(request.args.get('next') or url_for("admin.main"))
        flash("Invalid username or password")
    return render_template("/auth/login.html", form=form)


@auth.route("/logout")
@login_required
def logout():
    form = loginForm()
    logout_user()
    session["username"] = None
    flash("You have been logged out.")
    return render_template("/auth/login.html", form=form)


@auth.route("/register", methods=["GET", "POST"])
def register():
    form = registerForm()
    if form.validate_on_submit():
        user = User(email=form.email.data, username=form.username.data)
        user.password = form.password.data
        user.save()
        flash("You can login.")
        return redirect(url_for("auth.login"))
    return render_template("/auth/register.html", form=form)
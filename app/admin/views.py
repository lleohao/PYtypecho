from flask import render_template, redirect, request, url_for, abort, flash, session
from . import admin
from .forms import loginForm


@admin.route("/", methods=["GET"])
@admin.route("/login", methods=["GET", "POST"])
def login():
    form = loginForm()
    if form.validate_on_submit():
        name = form.username.data
        session["username"] = name
        pwd = form.password.data
        if name == "admin" and pwd == "admin":
            return redirect(url_for("admin.main"))
        else:
            flash("Username or Password error")
    return render_template("login.html", form=form)


@admin.route("/main")
def main():
    return "admin"


@admin.route("/register")
def register():
    return "register"
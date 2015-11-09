from flask import render_template, redirect, request,url_for, abort, flash
from flask.ext.login import login_required, current_user
from . import admin


@admin.route("/")
def index():
    return "hello world"

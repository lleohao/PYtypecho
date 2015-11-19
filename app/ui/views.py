from flask import render_template, redirect, flash, request, url_for
from flask.ext.login import login_required
from . import ui
from ..modules import Post


@ui.route("/")
def index():
    posts = Post.objects()
    return render_template("/ui/index.html", posts=posts )
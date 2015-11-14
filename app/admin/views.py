from flask import render_template, redirect, flash, request
from flask.ext.login import login_required
from . import admin


@admin.route("/main")
@login_required
def main():
    return render_template("/admin/main.html")


@admin.route("/main/addPost", methods=["GET", "POST"])
@login_required
def addPost():
    if request.method == "POST":
        return "<pre>" + request.form["test-editormd-markdown-doc"] + "<pre>"
    return render_template("/admin/addPost.html")

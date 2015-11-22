# coding: utf-8
from flask import render_template, redirect, flash, request, url_for, session
from flask.ext.login import login_required
from . import admin
from .forms import postForm, pageForm
from ..modules import Post, Page


@admin.route("/main")
@login_required
def main():
    return render_template("admin/main.html")


@admin.route("/main/write-post/", methods=["GET", "POST"])
@login_required
def write_post():
    form = postForm()
    if form.validate_on_submit():
        title = form.title.data
        slug = form.slug.data
        text = request.form["edit-area-markdown-doc"]
        tags = form.tags.data.split(",")
        author = session["username"]
        post = Post(title=title, slug=slug, text=text, tags=tags, author=author)
        if request.form["submit"] == "save":
            post.status = False
            post.save()
            if slug == "":
                post.slug = str(post.id)
                post.save()
            flash(u"保存草稿成功", "success")
            return redirect(url_for("admin.write_post"))
        else:
            post.status = True
            post.save()
            if slug == "":
                post.slug = str(post.id)
                post.save()
            flash(u"发布文章成功", "success")
            return redirect(url_for("admin.write_post"))
    return render_template("admin/write-post.html", form=form)


@admin.route("/main/write-page/", methods=["GET", "POST"])
@login_required
def write_page():
    form = pageForm()
    if form.validate_on_submit():
        title = form.title.data
        slug = form.slug.data
        text = request.form["edit-area-markdown-doc"]
        author = session["username"]
        page = Page(title=title, slug=slug, text=text, author=author)
        if request.form["submit"] == "save":
            page.status = False
            page.save()
            if slug == "":
                page.slug = str(post.id)
                page.save()
            flash(u"保存草稿成功", "success")
            return redirect(url_for("admin.write_page"))
        else:
            page.status = True
            page.save()
            if slug == "":
                page.slug = str(post.id)
                page.save()
            flash(u"发布页面成功", "success")
            return redirect(url_for("admin.write_page"))
    return render_template("admin/write-page.html", form=form)

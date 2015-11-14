import random
import string
from flask import render_template, redirect, flash, request, url_for
from flask.ext.login import login_required
from . import admin
from .forms import addPostForm
from ..modules import Post


@admin.route("/main")
@login_required
def main():
    return render_template("/admin/main.html")


@admin.route("/main/addPost", methods=["GET", "POST"])
@login_required
def addPost():
    form = addPostForm()
    if form.is_submitted():
        slug = form.slug.data+"-"+getRandString()
        post = Post(title=form.title.data, slug=slug,
                    content=request.form["test-editormd-markdown-doc"])
        post.save()
        return redirect("/admin/main/showPost/" + slug)
    return render_template("/admin/addPost.html", form=form)


@admin.route("/main/showPost/<slug>", methods=["GET", "POST"])
@login_required
def showPost(slug=None):
    post = Post.objects(slug=slug).first()
    return render_template("/admin/showPost.html", post=post)


def getRandString():
    return string.join(random.sample(['a','b','c','d','e','f','g',
                                      'h','i','j','k','l','m','n',
                                      'o','p','q','r','s','u','v',
                                      'w','x','y','z'], 4)).replace(' ','')
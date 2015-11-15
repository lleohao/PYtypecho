from flask import render_template, redirect, flash, request, url_for
from flask.ext.login import login_required
from . import admin
from .forms import addPostForm, addCategoryForm
from ..modules import Post, Category


@admin.route("/main")
@login_required
def main():
    return render_template("/admin/main.html")


@admin.route("/main/addPost", methods=["GET", "POST"])
@login_required
def addPost():
    form = addPostForm()
    if form.is_submitted():
        slug = form.slug.data
        if slug[0] != "2":
            slug = form.getRandomSlug(slug)
        post = Post(title=form.title.data, slug=slug,
                    content=request.form["test-editormd-markdown-doc"])
        post.save()
        return redirect("/admin/main/showPost/" + slug)
    return render_template("/admin/addPost.html", form=form)


@admin.route("/main/managePost")
@login_required
def managePost():
    posts = Post.objects()
    return render_template("/admin/managePost.html", posts=posts)

@admin.route("/main/showPost/<slug>")
@login_required
def showPost(slug=None):
    post = Post.objects(slug=slug).first()
    return render_template("/admin/showPost.html", post=post)


@admin.route("/main/addCategory", methods=["GET", "POST"])
@login_required
def addCategory():
    form = addCategoryForm()
    if form.validate_on_submit():
        category = Category(name=form.name.data, short_name=form.short_name.data, description=form.description.data)
        return redirect(url_for("admin.manageCatrgory"))
    return render_template("/admin/addCategory.html", form=form)


@admin.route("/main/manageCategory")
@login_required
def manageCategory():
    categories = Category.objects()
    return render_template("/admin/manageCategory.html", categories=categories)
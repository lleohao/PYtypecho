# coding: utf-8
from flask import render_template, redirect, flash, request, url_for
from flask.ext.login import login_required
from . import ui
# TODO: 更改了模型， 需要重新编写
from ..modules import Content, Category, Options


@ui.route("/")
@ui.route("/page/<int:page>")
def index(page=1):
    site = Options.objects.first()
    posts = Content.objects(type="post", status=True)[(page-1)*5: page*5]
    pageinate = Content.objects.paginate(page=page, per_page=5)
    categories = Category.objects()
    for post in posts:
        post.created = post.created.strftime("%Y-%m-%d")
    return render_template("index.html", site=site, posts=posts, categories=categories, pageinate=pageinate)


@ui.route("/article/<slug>")
def show_aticle(slug):
    site = Options.objects().first()
    posts= Content.objects(slug=slug)
    categories = Category.objects()
    return render_template("index.html",
                           site=site, posts=posts, categories=categories)


@ui.route("/<slug>/")
def show_slug(slug):
    site = Options.objects().first()
    cat = Category.objects(slug=slug).first()
    posts= Content.objects(category=cat)
    categories = Category.objects()
    return render_template("index.html",
                           site=site, posts=posts, categories=categories)
    return slug


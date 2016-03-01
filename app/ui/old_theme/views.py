# coding: utf-8
from flask import render_template

from . import ui
# TODO: 更改了模型， 需要重新编写
from ..modules import Content, Category, Options


@ui.route("/")
@ui.route("/page/<int:page>")
def index(page=1):
    site = Options.objects.first()
    posts = Content.objects(type="post", status=True)[(page - 1) * 5: page * 5]
    pageinate = Content.objects.paginate(page=page, per_page=5)
    pages = Content.objects(type="page").order_by("+created")
    categories = Category.objects()
    for post in posts:
        post.created = post.created.strftime("%Y-%m-%d")
    return render_template("index.html", site=site, posts=posts, categories=categories, pageinate=pageinate,
                           pages=pages)


@ui.route("/article/<slug>")
def show_aticle(slug):
    site = Options.objects().first()
    posts = Content.objects(slug=slug)
    post = Content.objects(slug=slug).first()
    categories = Category.objects()
    pages = Content.objects(type="page").order_by("+created")
    return render_template("article.html",
                           site=site, post=post, posts=posts, categories=categories, pages=pages)


@ui.route("/<slug>/")
def show_page(slug):
    site = Options.objects().first()
    posts = Content.objects(slug=slug)
    post = Content.objects(slug=slug).first()
    categories = Category.objects()
    pages = Content.objects(type="page").order_by("+created")
    return render_template("article.html",
                           site=site, post=post, posts=posts, categories=categories, pages=pages)


@ui.route("/category/<slug>/")
@ui.route("/category/page/<int:page>")
def show_category(slug, page=1):
    site = Options.objects().first()
    cat = Category.objects(slug=slug).first()
    posts = Content.objects(category=cat)[(page - 1) * 5: page * 5]
    pageinate = Content.objects(category=cat).paginate(page=page, per_page=5)
    pages = Content.objects(type="page").order_by("+created")
    categories = Category.objects()
    return render_template("index.html", site=site, posts=posts, categories=categories, pageinate=pageinate,
                           pages=pages)

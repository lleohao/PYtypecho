# coding: utf-8
from flask import render_template

from app.modules import Options, Content, Category
from . import ui


# 主页， 附带页码
@ui.route("/")
@ui.route("/page/<int:page>")
def index(page=1):
    site = Options.objects().first()
    posts = Content.objects(type="post")[(page - 1) * 5: page * 5]
    pages = Content.objects(type="page")
    pagination = Content.objects(type="post").paginate(page=page, per_page=5)
    return render_template("index.html", site=site, posts=posts, pages=pages, pagination=pagination)


# 查看页面
@ui.route("/<slug>")
def show_page(slug):
    site = Options.objects().first()
    pages = Content.objects(type="page")
    page = Content.objects(slug=slug).first()
    return render_template("page.html", site=site, pages=pages, page=page)


# 查看文章
@ui.route("/post/<slug>")
def show_post(slug):
    site = Options.objects().first()
    pages = Content.objects(type="page")
    post = Content.objects(slug=slug).first()
    return render_template("post.html", site=site, pages=pages, post=post)


# 查看归档目录
@ui.route("/archive")
def show_archive_list():
    site = Options.objects().first()
    pages = Content.objects(type="page")
    posts = Content.objects()
    created_time = []
    for post in posts:
        created_time.append(post.created.strftime("%Y-%m-%d"))

    return render_template("archive_list.html", site=site, pages=pages, posts=posts, created_time=created_time)


# 查看分类下所有文章
@ui.route("/category/<slug>")
@ui.route("/categort/<slug>/page/<int:page>")
def show_category(slug, page=1):
    site = Options.objects().first()
    pages = Content.objects(type="page")
    category = Category.objects(slug=slug).first()
    title = '分类 "%s" 下的文章' % (category.name)
    posts = Content.objects(category=category)[(page - 1) * 5: page * 5]
    pagination = Content.objects(category=category).paginate(page=page, per_page=5)
    created_time = []
    for post in posts:
        created_time.append(post.created.strftime("%Y-%m-%d"))

    return render_template('archive.html', title=title, posts=posts, created_time=created_time, site=site, pages=pages,
                           pagination=pagination, slug=slug)


# 查看标签下所有文章
@ui.route("/tag/<slug>")
@ui.route("/tag/<slug>/page/<int:page>")
def show_tag(slug, page=1):
    site = Options.objects().first()
    pages = Content.objects(type="page")
    title = '标签 "%s" 下的文章' % slug
    posts = Content.objects(tags=slug)[(page - 1) * 5: page * 5]
    pagination = Content.objects(tags=slug).paginate(page=page, per_page=5)
    created_time = []
    for post in posts:
        created_time.append(post.created.strftime("%Y-%m-%d"))

    return render_template('archive.html', title=title, posts=posts, created_time=created_time, site=site, pages=pages,
                           pagination=pagination, slug=slug)

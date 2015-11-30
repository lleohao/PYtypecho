# coding: utf-8
from flask import render_template, redirect, flash, request, url_for
from flask.ext.login import login_required
from . import ui
# TODO: 更改了模型， 需要重新编写
# from ..modules import Post, Site, Category


# @ui.route("/")
# def index():
#     site = Site.objects().first()
#     posts= Post.objects()
#     categories = Category.objects()
#     return render_template("ui/index.html",
#                            site=site, posts=posts, categories=categories)
#
#
# @ui.route("/article/<slug>")
# def show_aticle(slug):
#     site = Site.objects().first()
#     posts= Post.objects(slug=slug)
#     categories = Category.objects()
#     return render_template("ui/index.html",
#                            site=site, posts=posts, categories=categories)
#
#
# @ui.route("/<slug>/")
# def show_other(slug):
#     site = Site.objects().first()
#     posts= Post.objects(category=slug)
#     categories = Category.objects()
#     return render_template("ui/index.html",
#                            site=site, posts=posts, categories=categories)
#

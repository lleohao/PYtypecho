# coding: utf-8
import math
from datetime import datetime

from flask import render_template, redirect, flash, request, url_for, session
from flask.ext.login import login_required, current_user

from . import admin
from .forms import postForm, pageForm, categoryForm, userForm, OptionGeneralForm
from ..modules import Category, User, Options, Content


@admin.route("/")
@admin.route("/main")
@login_required
def main():
    # 后台概要页面， 获取文章总数及网站设置内容
    post_nums = Content.objects(type="post").count()
    site_option = Options.objects.first()
    return render_template("main.html", post_nums=post_nums, site_option=site_option, current_user=current_user)


# 文章相关内容
@admin.route("/write-post/<cid>")
@admin.route("/write-post/", methods=["GET", "POST"])
@login_required
def write_post(cid=None):
    # url_for("admin.write_post", cid=post.id) ==> url?cid=56d30e9117a6030e248d007a
    # 为了兼容只能这么处理
    if request.args.get("cid"):
        cid = request.args.get("cid")

    # 创建 form 表单内容
    if cid:
        # 存在 cid 说明是在修改文章，将文章内容绑定到 form 表单中
        post = Content.objects(id=cid).first()
        form = postForm(post)
    else:
        # 不存在则设置默认样式
        form = postForm()
    # 为 category 表单赋值选择项
    categories = Category.objects()
    form.category.choices = [(cat.slug, cat.name) for cat in categories]

    # 处理保存草稿及发布文章
    if form.validate_on_submit():
        # 根据表单提交的 content_id 判断是否新建或者是修改文章
        # 这里再次判断是否是修改文章的原因是 form 表单提交的地址 cid 永远为 None
        # 所以无法通过 cid 来判断是否是修改文章
        if form.content_id.data:
            post = Content.objects(id=form.content_id.data).first()
        else:
            post = Content(type="post")
        post.set_val(form, "post")

        if request.form["submit"] == "save":
            post.status = False
            post.save()
            flash(u"保存草稿成功", "success")
            return redirect(url_for("admin.write_post", cid=post.id))
        else:
            post.status = True
            post.save()
            flash(u"发布文章成功", "success")
            return redirect(url_for("admin.manage_posts"))

    return render_template("write-post.html", form=form, current_user=current_user)


@admin.route("/manage-posts")
@admin.route("/manage-categories/page/<int:page>")
@login_required
def manage_posts(page=1):
    cat = request.args.get("category")
    if cat:
        cat = Category.objects(name=cat).first()
        posts = Content.objects(type="post", category=cat)[(page - 1) * 5: page * 5]
    else:
        posts = Content.objects(type="post")[(page - 1) * 5: page * 5]

    pageinate = Content.objects.paginate(page=page, per_page=5)
    categories = Category.objects()
    createds = []
    delays = []
    comment_count = []
    for post in posts:
        createds.append(post.created.strftime("%Y-%m-%d"))
        delay = math.ceil((datetime.now() - post.created).seconds / 60)
        delays.append(delay)
        comment_count.append(len(post.comments))
    return render_template("manage-posts.html", posts=posts, categories=categories,
                           delays=delays, createds=createds, comment_count=comment_count,
                           pageinate=pageinate, current_user=current_user)


@admin.route("/delete-posts", methods=["POST"])
@login_required
def delete_posts():
    cids = request.form.getlist('cid')
    for cid in cids:
        post = Content.objects(id=cid)
        post.delete()
    flash(u"文章删除成功", "success")
    return redirect(url_for('admin.manage_posts'))


# 页面相关内容
@admin.route("/write-page", methods=["GET", "POST"])
@admin.route("/write-page/<cid>/")
@login_required
def write_page(cid=None):
    # 兼容性写法
    if request.args.get("cid"):
        cid = request.args.get("cid")

    # 创建 form 表单内容
    if cid:
        # 存在 cid 说明是在修改页面，将文章内容绑定到 form 表单中
        page = Content.objects(id=cid).first()
        form = pageForm(page)
    else:
        form = pageForm()

    if form.validate_on_submit():
        if form.content_id.data:
            page = Content.objects(id=form.content_id.data).first()
        else:
            page = Content(type="page")
        page.set_val(form, "page")

        if request.form["submit"] == "save":
            page.status = False
            page.save()
            flash(u"保存草稿成功", "success")
            return redirect(url_for("admin.write_page", cid=page.id))
        else:
            page.status = True
            page.save()
            flash(u"发布页面成功", "success")
            return redirect(url_for("admin.manage_pages"))
    return render_template("write-page.html", form=form)


@admin.route("/manage-pages")
@admin.route("/manage-pages/page/<page>")
@login_required
def manage_pages(page=1):
    pages = Content.objects(type="page")[(page - 1) * 5: page * 5]
    pageinate = Category.objects.paginate(page=page, per_page=5)
    createds = []
    comment_num = []
    for page in pages:
        createds.append(page.created.strftime("%Y-%m-%d"))
        comment_num.append(len(page.comments))
    return render_template("manage-pages.html", pages=pages, pageinate=pageinate, createds=createds,
                           comment_num=comment_num, current_user=current_user)


@admin.route('/delete-pages', methods=["POST"])
@login_required
def delete_pages():
    cids = request.form.getlist('cid')
    for cid in cids:
        page = Content.objects(id=cid)
        page.delete()
    flash(u"页面删除成功", "success")
    return redirect(url_for('admin.manage_pages'))


# 分类相关
@admin.route("/manage-categories/")
@admin.route("/manage-categories/page/<int:page>")
@login_required
def manage_categories(page=1):
    keyword = request.args.get("keyword")
    if keyword:
        categories = Category.objects.search_text(keyword)
    else:
        categories = Category.objects[(page - 1) * 5: page * 5]
        pageinate = Category.objects.paginate(page=page, per_page=5)
    count = [Content.objects(category=category).count() for category in categories]
    return render_template("manage-categories.html", categories=categories, count=count, pageinate=pageinate)


@admin.route("/category", methods=["GET", "POST"])
@login_required
def category():
    cid = request.args.get("cid")

    if cid is not None:
        categories = Category.objects(id=cid)
        old_category = categories[0]
        form = categoryForm(name=old_category.name, slug=old_category.slug, description=old_category.description)
        return render_template("categories.html", form=form)

    form = categoryForm()
    if form.validate_on_submit():
        categories = Category(name=form.name.data, slug=form.slug.data, description=form.description.data)
        categories.save()
        flash(u"分类保存成功", "success")
        return redirect(url_for("admin.manage_categories"))
    return render_template("categories.html", form=form)


@admin.route("/delete-categories", methods=["POST"])
@login_required
def delete_categories():
    cids = request.form.getlist('cid')
    for cid in cids:
        category = Category.objects(id=cid)
        category.delete()
    flash(u"分类删除成功", "success")
    return redirect(url_for('admin.manage_categories'))


# 用户相关
@admin.route("/users", methods=["GET", "POST"])
@admin.route("/users/<cid>")
@login_required
def users(cid=None):
    form = userForm()
    if cid:
        change_user = User.objects(id=cid).first()
        form.user_id.data = cid
        form.username.data = change_user.username
        form.email.data = change_user.email
        form.screenName.data = change_user.screenName
        form.url.data = change_user.url
        form.group.data = change_user.group

    if form.validate_on_submit():
        if form.user_id.data:
            user = User.objects(id=form.user_id.data).first()
            user.username = form.username.data
            user.email = form.email.data
            user.password = form.password.data
            user.url = form.url.data
            user.screenName = form.screenName.data
            user.group = form.group.data
            user.save()
        else:
            user = User(username=form.username.data, password=form.password.data, email=form.email.data,
                        url=form.url.data, screenName=form.screenName.data, group=form.group.data)
            user.save()
        flash(u"用户添加成功", "success")
        return redirect(url_for("admin.manage_users"))
    return render_template("users.html", form=form)


@admin.route("/manage-users", methods=["GET", "POST"])
@admin.route("/manage-users/page/<page>")
@login_required
def manage_users(page=1):
    users = User.objects[(page - 1) * 5: page * 5]
    pageinate = User.objects.paginate(page=page, per_page=5)
    return render_template("manage-users.html", users=users, pageinate=pageinate)


@admin.route("/delete-users", methods=["GET", "POST"])
@login_required
def delete_users():
    uids = request.form.getlist('uid')
    for uid in uids:
        user = User.objects(id=uid).first()
        if user.username == session['username']:
            flash("禁止删除正在登录的用户", "danger")
            return redirect(url_for('admin.manage_users'))
        else:
            user.delete()
    flash(u"用户删除成功", "success")
    return redirect(url_for('admin.manage_users'))


@admin.route("/manage-comments")
@login_required
def manage_comments():
    return "pass"


@admin.route('/options-general', methods=["GET", "POST"])
@login_required
def options_general():
    op = Options.objects.first()
    form = OptionGeneralForm(title=op.site_title,
                             url=op.site_url,
                             keyword=op.site_keyword,
                             description=op.site_description)

    if form.validate_on_submit():
        op.site_url = form.url.data
        op.site_title = form.title.data
        op.site_keyword = form.keyword.data
        op.site_description = form.description.data
        op.save()
        flash(u"网站信息保存成功", "success")
        return redirect(url_for("admin.options_general"))
    return render_template("options-general.html", form=form)

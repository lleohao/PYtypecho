# coding: utf-8
import math
from datetime import datetime
from flask import render_template, redirect, flash, request, url_for
from flask.ext.login import login_required
from . import admin
from .forms import ContentForm, categoryForm, userForm, OptionGeneralForm
from ..modules import Content, Category, User, Options


@admin.route("/")
@admin.route("/main")
@login_required
def main():
    page_num = Content.objects(type="post").count()
    op = Options.objects.first()
    return render_template("main.html", page_num=page_num, op=op)


# 文章相关内容
@admin.route("/write-post/", methods=["GET", "POST"])
@admin.route("/write-post/<cid>")
@login_required
def write_post(cid=None):
    form = ContentForm()
    categories = Category.objects()
    form.category.choices = [(cat.slug, cat.name) for cat in categories]
    if cid:
        content = Content.objects(id=cid).first()
        form.title.data = content.title
        form.slug.data = content.slug
        text = content.text
        category = content.category.name
        form.tags.data = str(content.tags).join(",")
        form.content_id.data = cid
    else:
        pass


    if form.validate_on_submit():
        content_id = form.content_id.data
        title = form.title.data
        slug = form.slug.data
        text = request.form["edit-area-markdown-doc"]
        tags = form.tags.data.split(",")
        category = Category.objects(slug=form.category.data).first()

        if content_id:
            post = Content.objects(id=content_id).first()
            post.title = title
            post.slug = slug
            post.text = text
            post.tags = tags
            post.category = category
        else:
            post = Content(title=title, slug=slug, text=text, tags=tags, category=category, type="post")

        if request.form["submit"] == "save":
            post.status = False
            post.save()
            form.content_id.data = post.id
            if slug == "":
                post.slug = str(post.id)
                form.slug.data = str(post.id)
                post.save()
            flash(u"保存草稿成功", "success")
            # FIXME: 这样会存在刷新多次提交的问题，后期需要改进
            return render_template("write-post.html", form=form, content=text)
        else:
            post.status = True
            post.save()
            form.content_id.data = post.id
            if slug == "":
                post.slug = str(post.id)
                form.slug.data = str(post.id)
                post.save()
            flash(u"发布文章成功", "success")
            return redirect(url_for("admin.manage_posts"))
    return render_template("write-post.html", form=form, categories=categories, content=text)


@admin.route("/manage-posts")
@admin.route("/manage-categories/page/<int:page>")
@login_required
def manage_posts(page=1):
    cat = request.args.get("category")
    if cat:
        cat = Category.objects(name=cat).first()
        posts = Content.objects(type="post", category=cat)[(page-1)*5: page*5]
    else:
        posts = Content.objects(type="post")[(page-1)*5: page*5]

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
                           pageinate=pageinate)


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
    form = ContentForm()
    if cid:
        content = Content.objects(id=cid).first()
        form.title.data = content.title
        form.slug.data = content.slug
        text = content.text
        form.content_id.data = cid
    else:
        pass

    if form.validate_on_submit():
        content_id = form.content_id.data
        title = form.title.data
        slug = form.slug.data
        text = request.form["edit-area-markdown-doc"]

        if content_id:
            page = Content.objects(id=content_id).first()
            page.title = title
            page.slug = slug
            page.text = text
        else:
            page = Content(title=title, slug=slug, text=text, type="page")

        if request.form["submit"] == "save":
            page.status = False
            page.save()
            form.content_id.data = page.id
            flash(u"保存草稿成功", "success")
            # FIXME: 这样会存在刷新多次提交的问题，后期需要改进
            return render_template("write-page.html", form=form, content=text)
        else:
            page.status = True
            page.save()
            form.content_id.data = page.id
            flash(u"发布页面成功", "success")
            return redirect(url_for("admin.manage_pages"))
    return render_template("write-page.html", form=form, content=text)


@admin.route('/manage-pages')
@login_required
def manage_pages():
    pages = Content.objects(type="page")
    createds = []
    comment_num = []
    for page in pages:
        createds.append(page.created.strftime("%Y-%m-%d"))
        comment_num.append(len(page.comments))
    return render_template("manage-pages.html", pages=pages, createds=createds, comment_num=comment_num)


@admin.route('/delete-pages', methods=["POST"])
@login_required
def delete_pages():
    slugs = request.form.getlist('slug')
    for slug in slugs:
        page = Content.objects(slug=slug)
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
        categories = Category.objects[(page-1)*5: page*5]
        pageinate = Category.objects.paginate(page=page, per_page=5)
    count = [Content.objects(category=category).count() for category in categories]
    return render_template("manage-categories.html", categories=categories, count=count, pageinate=pageinate)


@admin.route("/category", methods=["GET", "POST"])
@login_required
def category():
    # TODO: 修复分类不能添加
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
@login_required
def users():
    form = userForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, password=form.password.data, email=form.email.data, url=form.url.data, screenName=form.screenName.data, group=form.group.data)
        user.save()
        flash(u"用户添加成功", "success")
        return redirect(url_for("admin.manage_users"))
    return render_template("admin/users.html", form=form)


@admin.route("/manage-users", methods=["GET", "POST"])
@login_required
def manage_users():
    users = User.objects()
    return render_template("admin/manage-users.html", users=users)


@admin.route("/delete-users", methods=["GET", "POST"])
@login_required
def delete_users():
    uids = request.form.getlist('uid')
    for uid in uids:
        user = User(id=uid)
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





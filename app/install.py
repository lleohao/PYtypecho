# coding: utf-8
from .modules import Category, Options, User


def install():
    User(username="admin", password="admin", email="admin@admin.com", url="admin.admin", screenName="admin",
         group="administrator").save()
    Category(name="默认分类", slug="normal", description="这是系统默认的分类").save()
    Options(url="http://test_url.url", title="test_blog", keyword="blog,python,mongodb", description="test_blog_description").save()

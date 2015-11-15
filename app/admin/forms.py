# -*- coding:utf-8 -*-
import random, string
from datetime import date
from flask.ext.wtf import Form
from wtforms import StringField, SubmitField, PasswordField, BooleanField, TextAreaField
from wtforms.validators import InputRequired, Length, Email, Regexp, EqualTo


class addPostForm(Form):
    title = StringField(u"标题", validators=[InputRequired()])
    slug = StringField(u"Slug", default=date.today())
    submit = SubmitField(u"发布文章")

    def getRandomSlug(self, slug):
        return slug + '-' + string.join(random.sample(['a','b','c','d','e','f','g',
                                          'h','i','j','k','l','m','n',
                                          'o','p','q','r','s','u','v',
                                          'w','x','y','z'], 4)).replace(' ','')


class addCategoryForm(Form):
    name = StringField(u"分类名称*", validators=[InputRequired()])
    short_name = StringField(u"缩略名")
    description = TextAreaField(u"分类描述")
    submit = SubmitField(u"增加分类")
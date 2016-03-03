# -*- coding:utf-8 -*-
from flask.ext.wtf import Form
from flask.ext.wtf.html5 import EmailField, URLField
from wtforms import StringField, SubmitField, PasswordField, TextAreaField, SelectField, HiddenField
from wtforms.validators import InputRequired, EqualTo


class postForm(Form):
    content_id = HiddenField()
    title = StringField(u"标题", validators=[InputRequired()])
    slug = StringField(u"Slug")
    tags = StringField(u"标签")
    content = TextAreaField()
    category = SelectField(u"选择分类")

    def __init__(self, content=None):
        super(postForm, self).__init__()
        if content:
            self.content_id.data = content.id
            self.title.data = content.title
            self.slug.data = content.slug
            self.content.data = content.md_text
            self.category.data = content.category.slug
            if len(content.tags) > 0:
                self.tags.data = ",".join(content.tags)


class pageForm(Form):
    content_id = HiddenField()
    title = StringField(u"标题", validators=[InputRequired()])
    slug = StringField(u"Slug")
    content = TextAreaField()

    def __init__(self, content=None):
        super(pageForm, self).__init__()
        if content:
            self.content_id.data = content.id
            self.title.data = content.title
            self.slug.data = content.slug
            self.content.data = content.md_text


class categoryForm(Form):
    category_id = HiddenField()
    name = StringField(u"分类名称*", validators=[InputRequired()])
    slug = StringField(u"分类缩略名*", description=u"分类缩略名用于创建友好的链接形式, 建议使用字母, 数字, 下划线和横杠", validators=[InputRequired()])
    description = TextAreaField(u"分类描述", description=u"此文字用于描述分类, 在有的主题中它会被显示.")
    submit = SubmitField(u"保存分类")

    def __init__(self, category=None):
        super(categoryForm, self).__init__()
        if category:
            self.category_id.data = category.id
            self.name.data = category.name
            self.slug.data = category.slug
            self.description.data = category.description


class userForm(Form):
    choices = [
        ("subscriber", u"关注者"),
        ("editor", u"编辑"),
        ("administrator", u"管理员"),

    ]

    user_id = HiddenField()
    username = StringField(u"用户名*", validators=[InputRequired()],
                           description=u"此用户名将作为用户登录时所用的名称.<br>请不要与系统中现有的用户名重复.")
    email = EmailField(u"电子邮件*", validators=[InputRequired()],
                       description=u"电子邮箱地址将作为此用户的主要联系方式.<br>请不要与系统中现有的电子邮箱地址重复.")
    screenName = StringField(u"用户昵称",
                             description=u"用户昵称可以与用户名不同, 用于前台显示.<br>如果你将此项留空, 将默认使用用户名.")
    password = PasswordField(u"用户密码*", validators=[InputRequired(), EqualTo("password2", message="密码不相同")],
                             description=u"为此用户分配一个密码.<br>建议使用特殊字符与字母、数字的混编样式,以增加系统安全性.")
    password2 = PasswordField(u"用户密码确认*", validators=[InputRequired()],
                              description=u"请确认你的密码, 与上面输入的密码保持一致.")
    url = StringField(u"用户主页",
                      description=u"此用户的个人主页地址, 请用 http:// 开头.")
    group = SelectField(u"用户组", choices=choices, default=["subscriber"],
                        description=u"不同的用户组拥有不同的权限.<br>具体的权限分配表请<a href=\"#\">参考这里</a>.")
    submit = SubmitField(u"新增用户")

    def __init__(self, user=None):
        super(userForm, self).__init__()
        if user:
            self.user_id.data = user.id
            self.username.data = user.username
            self.email.data = user.email
            self.screenName.data = user.screenName
            self.url.data = user.url
            self.group.data = user.group


class OptionGeneralForm(Form):
    title = StringField(u"网站标题", description=u"站点的名称将显示在网页的标题处.")
    url = URLField(u"网站地址", description=u"站点地址主要用于生成内容的永久链接.")
    description = StringField(u"网站描述", description=u"站点描述将显示在网页代码的头部.")
    keyword = StringField(u"关键字", description=u"请以半角逗号\",\"分割多个关键字.")
    duoshuo_name = StringField(u"多说short_name", description=u"请填写你的多说short_name")
    submit = SubmitField(u"保存设置")

    def __init__(self, option=None):
        super(OptionGeneralForm, self).__init__()
        if option:
            self.title.data = option.title
            self.url.data = option.url
            self.keyword.data = option.keyword
            self.description.data = option.description
            self.duoshuo_name.data = option.duoshuo_name

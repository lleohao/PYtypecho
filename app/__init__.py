# coding: utf-8
from flask import Flask
from flask.ext.bootstrap import Bootstrap
from flask.ext.mongoengine import MongoEngine
from flask.ext.login import LoginManager
from flask.ext.wtf import CsrfProtect
from config import config

bootstrap = Bootstrap()
csrf = CsrfProtect()
login_manager = LoginManager()
login_manager.session_protection = "strong"
login_manager.login_view = "auth.login"
login_manager.login_message_category = "warning"
login_manager.login_message = u"您必须登录后才能访问这个页面"
db = MongoEngine()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    bootstrap.init_app(app)
    csrf.init_app(app)
    login_manager.init_app(app)
    db.init_app(app)

    # 导入用户验证模块
    from .auth import auth as auth_blueprint
    from .admin import admin as admin_blueprint
    from .ui import ui as ui_blueprint
    app.register_blueprint(auth_blueprint, url_prefix="/auth")
    app.register_blueprint(admin_blueprint, url_prefix="/admin")
    app.register_blueprint(ui_blueprint)

    return app

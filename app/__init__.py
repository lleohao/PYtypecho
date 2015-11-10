from flask import Flask
from flask.ext.bootstrap import Bootstrap
from flask.ext.login import LoginManager
from flask.ext.pymongo import PyMongo
from config import config

mongo = PyMongo()
bootstrap = Bootstrap()
login_manager = LoginManager()
login_manager.session_protection = "strong"
login_manager.login_view = "auth.login"


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    bootstrap.init_app(app)
    mongo.init_app(app)
    login_manager.init_app(app)

    from admin import admin as admin_blueprint
    app.register_blueprint(admin_blueprint)

    return app
import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KET = os.environ.get("SECRET_KEY") or "just so so"
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True

    @staticmethod
    def init_app(app):
        pass

    def __init__(self):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, "dev-database.db")


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, "database.db")


config = {
    "develop": DevelopmentConfig,
    "product": ProductionConfig,

    "default": DevelopmentConfig
}
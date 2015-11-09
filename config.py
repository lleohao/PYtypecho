import os

class Config:
    SECRET_KET = os.environ.get("SECRET_KEY") or "just so so"

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    MONGO_DBNAME = "devblog"


class ProductionConfig(Config):
    MONGO_DBNAME = "blog"


config = {
    "develop": DevelopmentConfig,
    "product": ProductionConfig,

    "default": DevelopmentConfig
}
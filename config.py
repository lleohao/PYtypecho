import os


class Config:
    SECRET_KEY = "abacd74f966611e5a00240f02fd6707c"
    BOOTSTRAP_SERVE_LOCAL = True

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    MONGODB_SETTINGS = {
        "DB": "devblog"
    }



class ProductionConfig(Config):
    MONGODB_SETTINGS = {
        "DB": "blog"
    }


config = {
    "develop": DevelopmentConfig,
    "product": ProductionConfig,

    "default": DevelopmentConfig
}
import os

from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired

basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))


class BaseConfig(object):
    SECRET_KEY = os.getenv("SECRET_KEY", "sjadfipuwehrovnw vweuhc asdknavortbisdp")
    BASE_DATABASE_URI = "sqlite:///" + os.path.join(basedir, "pepsi_yc")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    ASSERT_POST_PER_PAGE = 10
    ASSERT_MANAGE_POST_PER_PAGE = 15


class DevelopmentConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, "data-dev.db")


class TestingConfig(BaseConfig):
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"


class ProductionConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URI", "sqlite:///" + os.path.join(basedir, "assert.db")
    )


config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
}

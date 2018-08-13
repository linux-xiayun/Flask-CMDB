from random import random
import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    # 激活 跨站点请求伪造 保护
    CSRF_ENABLED = True
    # 设置secret key:为string格式
    SECRET_KEY = "flask cmdb"
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    FLASKY_MAIL_SUBJECT_PREFIX = '[CMDB]'
    FLASKY_MAIL_SENDER = '896365105@qq.com'
    FLASKY_ADMIN = os.environ.get('CMDB_ADMIN')

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    MAIL_SERVER = 'smtp.qq.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    #SQLALCHEMY_DATABASE_URI = "mysql+pymysql://myroot:'*xI*rUNBD0dsTKqS'@rm-2ze5yd90ukr81igd2no.mysql.rds.aliyuncs.com:3306/cmdb"
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URI') or \
                              'sqlite:///' + os.path.join(basedir, 'data-test.sqlite')


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI') or \
                              'sqlite:///' + os.path.join(basedir, 'data.sqlite')


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'Production': ProductionConfig,
    'default': DevelopmentConfig
}



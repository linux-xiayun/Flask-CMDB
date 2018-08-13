from flask import Flask,render_template,flash,url_for,redirect,Blueprint
from flask_bootstrap import Bootstrap
import logging
from flask_mail import Mail
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import *
from flask_openid import OpenID
import os
import sys


#解决flash的一个bug
defaultencoding = 'utf-8'
if sys.getdefaultencoding() != defaultencoding:
    reload(sys)
    sys.setdefaultencoding(defaultencoding)


logging.basicConfig(filename='cmdb.log', level=logging.ERROR)
logging.info('Started')
app = Flask(__name__)
logging.info('App established')
#读取config配置
app.config.from_object('config')
# 初始化Flask-Bootstap扩展
bootstrap = Bootstrap()
mail = Mail()
moment = Moment()


login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'cmdb.login'
oid = OpenID(app, os.path.join(basedir, 'tmp'))


app.config.from_object(config['default'])
config['default'].init_app(app)
bootstrap.init_app(app)
mail.init_app(app)
moment.init_app(app)
db = SQLAlchemy(app)
db.init_app(app)
login_manager.init_app(app)

from app import views, models




from flask import Flask
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flasgger import Swagger
from flask_sqlalchemy import SQLAlchemy
import pymysql
from flask_migrate import Migrate
from configs import config
import os
import datetime

default_setting = config.load_setting()
sqlalchemy_track_modifications = default_setting['config']['SQLALCHEMY_TRACK_MODIFICATIONS']
acc = default_setting['config']['db']['acc']
url_port = default_setting['config']['db']['url_port']
pw = default_setting['config']['db']['pw']
db_name = default_setting['config']['db']['db_name']
swagger_setting = default_setting['config']['swagger_setting']

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = sqlalchemy_track_modifications
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{acc}:{pw}@{url_port}/{db_name}"
app.config['SWAGGER'] = swagger_setting
app.config['SECRET_KEY'] = os.urandom(24)
# session有效期為1分鐘
app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(minutes=1)
bootstrap = Bootstrap(app)
moment = Moment(app)
# 建立swagger ui = localhost:5000/apidocs
Swagger(app)
# ORM工具
db = SQLAlchemy(app)
# 更新資料庫工具
migrate = Migrate(app, db)
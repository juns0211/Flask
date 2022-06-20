from flask import Flask
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flasgger import Swagger
from flask_sqlalchemy import SQLAlchemy
import pymysql
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:juns1984@localhost:3306/mydb"
app.config['SWAGGER'] = {
                            "title": "Swagger API",
                            "description": "Flask測試專用",
                            "version": "1.0.0",
                            "termsOfService": "",
                            "hide_top_bar": True
                        }
bootstrap = Bootstrap(app)
moment = Moment(app)
# 建立swagger ui = localhost:5000/apidocs
Swagger(app)
# ORM工具
db = SQLAlchemy(app)
# 更新資料庫工具
migrate = Migrate(app, db)
from flask import Flask, jsonify, request, make_response, redirect, abort, render_template
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from datetime import datetime
import pymysql
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flasgger import Swagger
from flask_swagger import swagger

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

@app.route('/')
def index():
    # user_agent = request.headers.get('User-Agent')
    # return f'<p>Your browser is {user_agent}</p>'

    # 建立status_code == 400
    #return '<h1>bad request</h1>', 400

    # 建立cookie
    # response = make_response('<h1>This document carries a cookie!</h1>')
    # response.set_cookie('answer', '42')
    # return response

    # 轉址
    #return redirect('http://google.com')

    # 轉譯模版
    return render_template('index.html', current_time=datetime.utcnow())

@app.route('/user/<name>')
def user(name):
    #return f"<h1>HelloWorld {name}</h1>"
    return render_template('user.html', name=name)

@app.route('/get_user/<id>')
def get_user(id):
    name = load_user(id)
    if not name:
        abort(404)
    return render_template('get_user.html', name=name)


def load_user(id):
    user_data = {'1':'juns','2':'verena','3':'william','4':'sain'}
    if id not in user_data.keys():
        return None
    return user_data[id]

#自訂錯誤網頁
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
#自訂錯誤網頁
@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

#swagger_api網頁
# @app.route("/spec")
# def swagger_spec():
#     return jsonify(swagger(app))
from swagger_api.url import swagger_api_app
app.register_blueprint(swagger_api_app, url_prefix='/api')

#test_api網頁
from test_api.url import test_api_app
app.register_blueprint(test_api_app, url_prefix='/api')

# if __name__ == '__main__':
#     app.run(debug=True)
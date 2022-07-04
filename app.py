from flask import jsonify, request, make_response, redirect, abort, render_template
from datetime import datetime
from flask_swagger import swagger
from setting import app
from flask_login import login_required, current_user


@app.route('/')
# 欄截請求, 並將使用者送到登入網頁
@login_required
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
    return render_template('index.html', current_time=datetime.utcnow(), name=current_user.acc)

@app.route('/user/<name>')
@login_required
def user(name):
    #return f"<h1>HelloWorld {name}</h1>"
    return render_template('user.html', name=name)

@app.route('/get_user/<id>')
@login_required
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

#user api
from user.url import user_api_app
app.register_blueprint(user_api_app, url_prefix='/api')

#login api
from login.url import login_api_app
app.register_blueprint(login_api_app)

if __name__ == '__main__':
    app.run(debug=True)

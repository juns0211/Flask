from flask import Flask, jsonify, request, make_response, redirect, abort, render_template, Response
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from datetime import datetime
from flask_swagger import swagger
import json
import pymysql
from flask_sqlalchemy import SQLAlchemy
from db import sql_db
import traceback

app = Flask('hello')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:juns1984@localhost:3306/mydb"
bootstrap = Bootstrap(app)
moment = Moment(app)
db = SQLAlchemy(app)

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

#開post_API
@app.route("/test", methods=['POST'])
def test_post():
    try:
        insert = request.get_json()
        user = insert['name']
        if insert.get('id'):
            id = insert['id']
            obj = sql_db.mysql_db(**{'id':id, 'name':user})
        else:
            obj = sql_db.mysql_db(**{'name':user})
        sql_db.db.session.add(obj)
        sql_db.db.session.commit()
        return Response(json.dumps({'success':True, 'message':'', 'data':{'name':user, 'id':id} if insert.get('id') else {'name':user}}, ensure_ascii=False), status=200, mimetype='application/json')
    except KeyError:
        print('\n' + traceback.format_exc())
        return Response(json.dumps({'success':False, 'message':'請檢查傳入參數是否缺少', 'data':{}}, ensure_ascii=False),status=401, mimetype='application/json')
    except Exception:
        print('\n' + traceback.format_exc())
        return Response(json.dumps({'success':False, 'message':'未知錯誤', 'data':{}}, ensure_ascii=False),status=401, mimetype='application/json')

#開post_API
@app.route("/test", methods=['GET'])
def test_get():
    try:
        insert = request.get_json()
        id = insert['id']
       # result = sql_db.db.session.query(sql_db.mysql_db).filter_by(id=id).first()
        result = sql_db.mysql_db.query.filter_by(id=id).first()
        if not result:
            return Response(json.dumps({'success':True, 'message':'', 'data':{}}, ensure_ascii=False), status=200, mimetype='application/json')
        return Response(json.dumps({'success':True, 'message':'', 'data':{'name':result.name, 'id':id}}, ensure_ascii=False), status=200, mimetype='application/json')
    except KeyError:
        print('\n' + traceback.format_exc())
        return Response(json.dumps({'success':False, 'message':'請檢查傳入參數是否缺少', 'data':{}}, ensure_ascii=False),status=401, mimetype='application/json')
    except Exception:
        print('\n' + traceback.format_exc())
        return Response(json.dumps({'success':False, 'message':'未知錯誤', 'data':{}}, ensure_ascii=False),status=401, mimetype='application/json')

if __name__ == '__main__':
    app.run(debug=True)

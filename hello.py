from http.client import responses
from urllib import response
from flask import Flask, request, make_response, redirect, abort

app = Flask(__name__)

@app.route('/')
def index():
    user_agent = request.headers.get('User-Agent')
    return f'<p>Your browser is {user_agent}</p>'

    # 建立status_code == 400
    #return '<h1>bad request</h1>', 400

    # 建立cookie
    # response = make_response('<h1>This document carries a cookie!</h1>')
    # response.set_cookie('answer', '42')
    # return response

    # 轉址
    #return redirect('http://google.com')

@app.route('/user/<name>')
def user(name):
    return f"<h1>HelloWorld {name}</h1>"

@app.route('/get_user/<id>')
def get_user(id):
    user = load_user(id)
    if not user:
        abort(404)
    return f'<h1>hello, 西擺{user}'


def load_user(id):
    user_data = {'1':'juns','2':'verena','3':'william','4':'sain'}
    if id not in user_data.keys():
        return None
    return user_data[id]

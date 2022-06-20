from flask import Blueprint
from . import view

# Flask多資料夾結構工具
user_api_app = Blueprint('user_api_app', __name__)
user_api_app.add_url_rule('/user', 'test view', view_func=view.user_view.as_view('test view'))
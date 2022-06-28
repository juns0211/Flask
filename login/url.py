from flask import Blueprint
from . import view

# Flask多資料夾結構工具
login_api_app = Blueprint('login_api_app', __name__)
login_api_app.add_url_rule('/login', 'login view', view_func=view.login_view.as_view('login view'))
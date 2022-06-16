from flask import Blueprint
from . import view

# Flask多資料夾結構工具
test_api_app = Blueprint('test_api_app', __name__)
test_api_app.add_url_rule('/user', 'test view', view_func=view.test_view.as_view('test view'))
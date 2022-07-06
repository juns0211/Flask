from flask import Blueprint
from . import view

# Flask多資料夾結構工具
upload_api_app = Blueprint('upload_api_app', __name__)
upload_api_app.add_url_rule('/upload_data', 'upload view', view_func=view.upload_view.as_view('upload view'))
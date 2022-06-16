from flask import Blueprint
from . import view


# Flask多資料夾結工具
swagger_api_app = Blueprint('swagger_api_app', __name__)
swagger_api_app.add_url_rule('/swagger_api', 'swagger view', view_func=view.swagger_view.as_view('swagger view'))
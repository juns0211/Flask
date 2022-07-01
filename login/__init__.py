from flask_login import LoginManager
from setting import app
from flask import Blueprint
from . import view

# Flask多資料夾結構工具
login_api_app = Blueprint('login_api_app', __name__)
#login_api_app.add_url_rule('/login', 'login view', view_func=view.login_view.as_view('login view'))

login_manager = LoginManager()
# 設定登入網頁端點, 當未登入狀態使用者, 進入受保護網頁時, 轉扯到登入頁
login_manager.login_view = 'login_api'
login_manager.init_app(app)

# 註冊藍圖路由位置失敗, 待驗證原因
def create_app(config_name):
    app.register_blueprint(login_api_app, url_prefix='/auth')
    return app


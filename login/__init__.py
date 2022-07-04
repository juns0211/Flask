from flask_login import LoginManager
from setting import app

login_manager = LoginManager()
# 設定登入網頁端點, 當未登入狀態使用者, 進入受保護網頁時, 轉扯到登入頁
login_manager.login_view = 'login_api_app.login view'
login_manager.init_app(app)


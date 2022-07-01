
from setting import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from login import login_manager

class mysql_db(UserMixin, db.Model):
    __tablename__ = 'user'
    #API欄位 autoincrement自動產生值
    acc = db.Column(db.Text, autoincrement=True, primary_key=True)
    name = db.Column(db.Text)
    password_hash = db.Column(db.String(128))


    def to_dict(self):
        return {col.name: getattr(self, col.name) for col in self.__table__.columns}

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    @login_manager.user_loader
    def load_user(user_id):
        return mysql_db.query.get(user_id)
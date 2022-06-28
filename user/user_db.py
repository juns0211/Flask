
from setting import db



class mysql_db(db.Model):
    __tablename__ = 'user'
    #API欄位 autoincrement自動產生值
    acc = db.Column(db.Text, autoincrement=True, primary_key=True)
    name = db.Column(db.Text)
    password = db.Column(db.Text)


    def to_dict(self):
        return {col.name: getattr(self, col.name) for col in self.__table__.columns}

from hello import db



class mysql_db(db.Model):
    __tablename__ = 'test'
    #API欄位
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)

    def to_dict(self):
        return {col.name: getattr(self, col.name) for col in self.__table__.columns}
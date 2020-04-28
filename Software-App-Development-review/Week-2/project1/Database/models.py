import sys
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "users"
    name = db.Column(db.String, primary_key=True)
    password = db.Column(db.String, nullable=False)
    timestamp = db.Column(db.Integer, nullable=False)



# time.ctime(calendar.timegm(time.gmtime()))
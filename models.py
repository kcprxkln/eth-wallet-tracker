from flask_login import UserMixin
from sqlalchemy.sql import func 
from testy import db 

class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(1000), unique=True)
    password = db.Column(db.String(1000))
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    followed_wallets = db.relationship('Wallets') 

class Wallets(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(1000))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
from flask_login import UserMixin
from sqlalchemy.sql import func 
from db_operations import db 

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(200))
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    followed_wallets = db.relationship('Wallet') 

class Wallet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
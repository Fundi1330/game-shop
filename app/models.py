from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

class User(UserMixin, db.Model):
    __tablename__ = 'Users'
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(120), index = True, unique = True)
    email = db.Column(db.String(60), index = True, unique = True)
    password_hash = db.Column(db.String(120))
    admin = db.Column(db.Boolean, index = True, default=False)
    cart = db.Column(db.String)


    def __repr__(self) -> str:
        return '<User {}'.format(self.username)
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Game(UserMixin, db.Model):
    __tablename__ = 'Game'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(40), index = True, unique=True)
    descreption = db.Column(db.String(80), index = True)
    price = db.Column(db.Float, index=True)
    developer = db.Column(db.String)
    publisher = db.Column(db.String)
    release_date = db.Column(db.Date)
    genre = db.Column(db.String)
    ratings = db.Column(db.String, default='[]')
    
    def __repr__(self) -> str:
        return f'name: {self.name}, price: {self.price}'

from itertools import product
from makeup_app.extensions import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(80), nullable = False)
    password = db.Column(db.String(80), nullable=False)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(80), nullable = False)
    rating = db.Column(db.Integer, nullable = False)
    review = db.Column(db.Text, nullable = False)

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(80), nullable = False)
    comment = db.Column(db.String, nullable = False)
    prd = db.Column(db.Integer, nullable = False)
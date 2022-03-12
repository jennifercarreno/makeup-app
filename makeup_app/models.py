from itertools import product
from makeup_app.extensions import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(80), nullable = False)
    password = db.Column(db.String(80), nullable=False)

class Review(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    prd_name = db.Column(db.String(80), nullable = False)
    rating = db.Column(db.Integer, nullable = False)
    review = db.Column(db.Text, nullable = False)
    created_by_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_by = db.relationship('User')




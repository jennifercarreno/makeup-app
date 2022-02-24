from unicodedata import name
from wsgiref.validate import validator
from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SelectField, SubmitField, FloatField, PasswordField, IntegerField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired, Length, URL
from flask_bcrypt import bcrypt

from makeup_app.models import User, Product

class ProductForm(FlaskForm):
    """Form for adding a Product."""

    name = StringField('Name', validators=[DataRequired()])
    rating = IntegerField('Rating', validators=[DataRequired()])
    review = StringField('Review', validators=[DataRequired()])
    submit = SubmitField('Submit')

class CommentForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    comment = StringField('Comment', validators=[DataRequired()])
    submit = SubmitField('Submit')

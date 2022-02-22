from flask import Blueprint, request, render_template, redirect, url_for, flash
from makeup_app.models import User, Post, Comment
from makeup_app.extensions import app, db
# add forms

main = Blueprint("main", __name__)

@main.route('/')
def homepage():
    return render_template('home.html')
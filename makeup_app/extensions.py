from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from makeup_app.config import Config

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
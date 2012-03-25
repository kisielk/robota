from flask import Flask
from flaskext.sqlalchemy import SQLAlchemy

DEBUG = True
SECRET_KEY = 'secret'
USERNAME = 'kamil'
PASSWORD = 'kamil'
HOST = '0.0.0.0'
SQLALCHEMY_DATABASE_URI = 'sqlite:///state.db'

app = Flask(__name__)
app.config.from_object(__name__)
db = SQLAlchemy(app)

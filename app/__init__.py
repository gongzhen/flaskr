# all the imports

from flask.ext.sqlalchemy import SQLAlchemy 
from flask.ext.login import LoginManager
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
from contextlib import closing
import os

# configuration
# developer has to create table first by using python shell
# >>from flaskr import init_db
# >> init_db() table is crated
DATABASE = '/Users/gongzhen/Virtualenvs/helloworld/flaskr/flaskr.db' #C:\Projects\flask\flaskr
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'gongzhen'
PASSWORD = 'gongzhen'

# create our little application :)
app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_envvar('FLASKR_SETTING', silent=True)

db = SQLAlchemy()
login_manager = LoginManager()
db.init_app(app)
login_manager.init_app(app)

from app import views

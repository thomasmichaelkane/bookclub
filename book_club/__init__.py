from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
import jinja_partials
import random

## APP SETUP ##
DB_NAME = "site.db"

with open("secrets.txt") as f:
    SECRET_KEY = f.readline()

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
jinja_partials.register_extensions(app)

## LOGIN CONFIG ##
login_manager = LoginManager(app)
login_manager.login_view = 'auth.login'
login_manager.login_manager_category = 'info'

## BLUEPRINTS ##
from book_club.views import views
from book_club.auth import auth
from book_club.actions import actions

app.register_blueprint(views, url_prefix='/')
app.register_blueprint(auth, url_prefix='/')
app.register_blueprint(actions, url_prefix='/')

## JINJA CONFIG ##
from book_club.utils import BookStatusEnum, get_iterables_dict, band_generator

@app.template_filter('shuffle')
def filter_shuffle(seq):
    try:
        result = list(seq)
        random.shuffle(result)
        return result
    except:
        return seq
    
@app.template_filter('next_item')
def next_item(seq):
    return next(seq)

app.jinja_env.globals.update(get_iterables_dict=get_iterables_dict)
app.jinja_env.globals.update(band_generator=band_generator)
app.jinja_env.globals.update(BookStatusEnum=BookStatusEnum)


    
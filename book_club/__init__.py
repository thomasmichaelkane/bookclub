from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
import jinja_partials
import random

## APP SETUP ##
DB_NAME = "site.db"

app = Flask(__name__)
app.config['SECRET_KEY'] = 'pascal'
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
from book_club.library import random_book_color
from book_club.utils import BookStatusEnum

@app.template_filter('shuffle')
def filter_shuffle(seq):
    try:
        result = list(seq)
        random.shuffle(result)
        return result
    except:
        return seq

app.jinja_env.globals.update(random_book_color=random_book_color)
app.jinja_env.globals.update(BookStatusEnum=BookStatusEnum)


    
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
import jinja_partials
import random
# import json

DB_NAME = "site.db"

app = Flask(__name__)
app.config['SECRET_KEY'] = 'pascal'
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
jinja_partials.register_extensions(app)

login_manager = LoginManager(app)
login_manager.login_view = 'auth.login'
login_manager.login_manager_category = 'info'

from book_club.views import views
from book_club.auth import auth
from book_club.retr import retr
from book_club.custom_filters import random_book_color

app.register_blueprint(views, url_prefix='/')
app.register_blueprint(auth, url_prefix='/')
app.register_blueprint(retr, url_prefix='/')

@app.template_filter('shuffle')
def filter_shuffle(seq):
    try:
        result = list(seq)
        random.shuffle(result)
        return result
    except:
        return seq
    
app.jinja_env.globals.update(random_book_color=random_book_color)

# def create_database(app):
#     if not os.path.exists('flask_web/' + DB_NAME):
#         with app.app_context():
#             db.create_all()
#         print('Database')



# from book_club.models import User, Note





    
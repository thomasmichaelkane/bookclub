from book_club import db, login_manager
from book_club.utils import BookStatusEnum, ArticleTypeEnum
from flask_login import UserMixin
from datetime import datetime, timezone

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
    
class Book(db.Model):
    __tablename__ = "book"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(1000), nullable=False)
    author = db.Column(db.String(1000), nullable=False)
    description = db.Column(db.String(10000))
    olid = db.Column(db.String(100), nullable=False)
    cover_url_s = db.Column(db.String(1000))
    cover_url_m = db.Column(db.String(1000))
    cover_url_l = db.Column(db.String(1000))
    user_relationships = db.relationship('BookUserRel', backref='book')
    average_rating = db.Column(db.Float, default=None)
    
    def __repr__(self):
        return f"Book('{self.title}', '{self.author}', '{self.olid}')"
    
class User(db.Model, UserMixin):
    _name__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    book_relationships = db.relationship('BookUserRel', backref='user')
    articles = db.relationship('Article', backref='user')
    
    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

class BookUserRel(db.Model):
    _name__ = "book_user_rel"
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.Enum(BookStatusEnum), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    review = db.Column(db.String(1000))
    rating = db.Column(db.Float, default=None)
    favourite = db.Column(db.Boolean, default=False, nullable=False)
    
    def __repr__(self):
      return f"BookUserRel('{self.book.title}', '{self.user.username}', '{self.status}')"
  
class Article(db.Model):
    _name__ = "article"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    type = db.Column(db.Enum(ArticleTypeEnum), nullable=False)
    content = db.Column(db.String(10000), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    images = db.Column(db.String(1000))
    thumbnail = db.Column(db.String(1000))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    def __repr__(self):
        return f"Article('{self.user_author}', '{self.email}')"
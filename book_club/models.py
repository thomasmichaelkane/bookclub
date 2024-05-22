from book_club import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
    
class Book(db.Model):
    __tablename__ = "book"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(1000))
    author = db.Column(db.String(1000))
    olid = db.Column(db.String(100))
    cover_url_s = db.Column(db.String(1000))
    cover_url_m = db.Column(db.String(1000))
    cover_url_l = db.Column(db.String(1000))
    users_wish = db.relationship('User', secondary='books_wish', back_populates='books_wish')
    users_read = db.relationship('User', secondary='books_read', back_populates='books_read')
    users_reading = db.relationship('User', secondary='books_reading', back_populates='books_reading')
    reviews = db.relationship('Review', backref='book')
    # average rating
    
class Review(db.Model):
    _name__ = "review"
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(500))
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'))
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    # date posted
    # rating
    
class User(db.Model, UserMixin):
    _name__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    books_wish = db.relationship('Book', secondary='books_wish', back_populates='users_wish')
    books_read = db.relationship('Book', secondary='books_read', back_populates='users_read')
    books_reading = db.relationship('Book', secondary='books_reading', back_populates='users_reading')
    reviews = db.relationship('Review', backref='author')
    # books = db.relationship('Book', backref='reader', lazy=True)
    # date joined
    
    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"
    
#join tables
books_wish = db.Table(
  'books_wish',
  db.Column('book_id', db.Integer, db.ForeignKey('user.id')),
  db.Column('user_id', db.Integer, db.ForeignKey('book.id'))
)

books_read = db.Table(
  'books_read',
  db.Column('book_id', db.Integer, db.ForeignKey('user.id')),
  db.Column('user_id', db.Integer, db.ForeignKey('book.id'))
)

books_reading = db.Table(
  'books_reading',
  db.Column('book_id', db.Integer, db.ForeignKey('user.id')),
  db.Column('user_id', db.Integer, db.ForeignKey('book.id'))
)
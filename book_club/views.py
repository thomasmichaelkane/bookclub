from flask import Blueprint, render_template
from flask_login import login_required, current_user
from book_club.models import Book, User, BookUserRel, Article
from book_club.forms import BookForm, ReviewForm
from book_club.library import search_book

views = Blueprint('views', __name__)

## HOME PAGE ##
@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    
    users = User.query.all()
    books = Book.query.all()
    articles = Article.query.all()
            
    return render_template('home.html', users=users, books=books, articles=articles)

## BOOK PAGE ##
@views.route('/book/<int:book_id>', methods=['GET', 'POST'])
@login_required
def book(book_id):
    
    book = Book.query.get_or_404(book_id)

    current_user_relationship = BookUserRel.query.filter(BookUserRel.book==book, BookUserRel.user==current_user).first()
      
    form = ReviewForm()
    
    return render_template('book.html', book=book, form=form, relationship=current_user_relationship)

## ARTICLE PAGE ##
@views.route('/article/<int:article_id>', methods=['GET', 'POST'])
@login_required
def article(article_id):
    
    article = Article.query.get_or_404(article_id)

    return render_template('article.html', article=article)

## USER PAGE ##
@views.route('/user/<int:user_id>', methods=['GET', 'POST'])
@login_required
def user(user_id):
    
    user = User.query.get_or_404(user_id)
    
    return render_template('user.html', user=user, title=user.username)

## MY LIBRARY PAGE ##
@views.route('/my-library', methods=['GET', 'POST'])
@login_required
def my_library():
    return render_template('user.html', user=current_user, title="My Library")

## SEARCH PAGE ##
@views.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    form = BookForm()
    if form.validate_on_submit():
        
        book_api = search_book(form.title.data, form.author.data)
        
        if book_api is not None:
            book_api_olid = book_api["olid"]
            book = Book.query.filter_by(olid=book_api_olid).first()
            exists = bool(book)

        if exists:
            return render_template('search.html', form=form, book=book, book_api=book_api, exists=exists)
        else:
            return render_template('search.html', form=form, book_api=book_api, exists=exists)
    return render_template('search.html', form=form)

## RECCOMEND PAGE ##
@views.route('/reccomend', methods=['GET', 'POST'])
@login_required
def reccomend():
    return render_template('reccomend.html', response=[])

## ARTICLES PAGE ##
@views.route('/articles', methods=['GET', 'POST'])
@login_required
def articles():
    
    articles = Article.query.all()

    return render_template('articles.html', articles=articles)
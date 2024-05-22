from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
import requests
from book_club import db
from book_club.models import Book
from book_club.forms import ReviewForm
from book_club.aiapi import response_test
from book_club.library import search_book, search_by_olid

actions = Blueprint('actions', __name__)

## WISHLIST BOOK ##
@actions.route('/wishlist-book', methods=['POST'])
@login_required
def wishlist_book():
    
    if request.method == 'POST':
        book_id = request.form.get('wish')
        book = Book.query.get_or_404(book_id)
        current_user.books_wish.append(book)
        db.session.commit()
    
        return render_template('/book.html', book=book, form=None)
    
## START BOOK ##
@actions.route('/start-book', methods=['POST'])
@login_required
def start_book():
    
    if request.method == 'POST':

        book_id = request.form.get('start')
        book = Book.query.get_or_404(book_id)
        
        if current_user in book.users_wish:
            current_user.books_wish.remove(book)
        
        if current_user not in book.users_reading:
            current_user.books_reading.append(book)
       
        db.session.commit()
    
        book = Book.query.get_or_404(book_id)
        return render_template('book.html', book=book, form=None)

## FINISH BOOK ##
@actions.route('/finish-book', methods=['POST'])
@login_required
def finish_book():
    
    if request.method == 'POST':
        
        book_id = request.form.get('finish')
        book = Book.query.get_or_404(book_id)
        
        if current_user in book.users_reading:
            current_user.books_reading.remove(book)
        if current_user in book.users_wish:
            current_user.books_wish.remove(book)
        if current_user not in book.users_read:
            current_user.books_read.append(book)
        db.session.commit()
        
        form = ReviewForm()
    
        return render_template('book.html', book=book, form=form)

## SHELVE BOOK ##
@actions.route('/shelve-book', methods=['POST'])
@login_required
def shelve_book():
    
    if request.method == 'POST':
        
        book_id = request.form.get('shelve')
        book = Book.query.get_or_404(book_id)
        
        if current_user in book.users_reading:
            current_user.books_reading.remove(book)
        if current_user in book.users_wish:
            current_user.books_wish.remove(book)
            
        db.session.commit()
    
        book = Book.query.get_or_404(book_id)
        return render_template('book.html', book=book, form=None)

## API BOOK ##
@actions.route('/find-book', methods=['POST'])
@login_required
def find_book():
    
    if request.method == 'POST':
        
        rec_info = request.form.get('rec')
        rec_title = rec_info[0]
        rec_author = rec_info[1]
        
        book_info = search_book(rec_title, rec_author)
        
        print(book_info)
        
## ADD BOOK PAGE ##
@actions.route('/add-book', methods=['GET', 'POST'])
@login_required
def add_book():
    
    if request.method == 'POST':
        
        olid = request.form.get('add')

        book = Book.query.filter_by(olid=olid).first()
        exists = bool(book)
        
        print(exists)
        
        if exists is not True:
        
            book_info = search_by_olid(olid)
            book = Book(title=book_info["title"], 
                        author=book_info["author"], 
                        olid=book_info["olid"],
                        cover_url_s=book_info["cover_url_s"], 
                        cover_url_m=book_info["cover_url_m"],
                        cover_url_l=book_info["cover_url_l"])

            db.session.add(book)
            flash(f'{book_info["title"]} added to book club!', category='success')

        db.session.commit()

        return render_template('book.html', book=book, form=None)

## GPT RECCOMEND ##
@actions.route('/gpt-reccomend', methods=['POST'])
@login_required
def gpt_reccomend():
    
    if request.method == 'POST':
        
        response = response_test()
    
    return render_template('reccomend.html', user=current_user, response=response)

## API TEST ##
@actions.route('/lotr_test', methods=['GET', 'POST'])
def lotr_test():
    
    api_response = requests.get('https://openlibrary.org/search.json?title=the+lord+of+the+rings').json()
    
    lotr = api_response["docs"][0]
    
    title = lotr["title"]
    author = lotr["author_name"]
    cover_id = lotr["cover_i"]
    img_url = f"https://covers.openlibrary.org/b/id/{cover_id}-M.jpg"
    
    print(title, author, img_url)
    
    return lotr

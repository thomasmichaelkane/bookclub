from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from book_club import db
from book_club.models import Book, Review, User
from book_club.forms import BookForm, ReviewForm
from book_club.book_func import book_in_lists
from book_club.aiapi import create_by_reading_prompt, rec_test, response_test
from book_club.retr import search_book

views = Blueprint('views', __name__)

## HOME PAGE ##
@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    
    users = User.query.all()
    books = Book.query.all()
    main_book_ids = {user.id: 0 for user in users}
    
    if request.method == 'POST':

        ids = request.form.get('switch_main_book')
        main_book_ids[ids[1]] = ids[4]
        print(main_book_ids)
            
    return render_template('home.html', users=users, books=books)

## RECCOMEND PAGE ##
@views.route('/reccomend', methods=['GET', 'POST'])
@login_required
def reccomend():
    return render_template('reccomend.html', response=[])

## RECCOMEND METHODS ##
@views.route('/rec_prompt', methods=['POST'])
@login_required
def rec_prompt():
    
    if request.method == 'POST':
        
        response = response_test()
    
    return render_template('reccomend.html', user=current_user, response=response)

@views.route('/find_book', methods=['POST'])
@login_required
def find_book():
    
    if request.method == 'POST':
        
        rec_info = request.form.get('rec')
        rec_title = rec_info[0]
        rec_author = rec_info[1]
        
        book_info = search_book(rec_title, rec_author)
        
        print(book_info)

## MY BOOKS PAGE ##
@views.route('/my-books', methods=['GET', 'POST'])
@login_required
def my_books():
    return render_template('my_books.html')

## SEARCH PAGE ##
@views.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    form = BookForm()
    if form.validate_on_submit():
        
        book_api = search_book(form.title.data, form.author.data)
        
        if book_api is not None:
            book_api_olid = book_api["olid"]
            exists = bool(Book.query.filter_by(olid=book_api_olid).first())
    
        return render_template('search.html', form=form, book_api=book_api, exists=exists)
    return render_template('search.html', form=form)

## ADD BOOK PAGE ##
@views.route('/add-book', methods=['GET', 'POST'])
@login_required
def add_book(book_info):
    
    if request.method == 'POST':
        
        book_info = request.form.get('rec')
    
        search_olid = book_info["openlib_api_info"]["olid"]
        exists = bool(Book.query.filter_by(olid=search_olid).first())
        
        print(exists)
        
        if exists is not True:
        
            book = Book(title=book_info["title"], 
                        author=book_info["author"], 
                        olid=book_info["olid"],
                        cover_url_s=book_info["cover_url_s"], 
                        cover_url_m=book_info["cover_url_m"],
                        cover_url_l=book_info["cover_url_l"])

            db.session.add(book)
        
        current_user.books_wishlist.append(book)
        db.session.commit()
        
        flash(f'{book_info["title"]} added to your wishlist!', category='success')

        return redirect(url_for('views.add_book'))

## BOOK PAGE ##
@views.route('/book/<int:book_id>', methods=['GET', 'POST'])
@login_required
def book(book_id):
    
    book = Book.query.get_or_404(book_id)
    
    if book in current_user.books_read:
        
        form = ReviewForm()
    
        if form.validate_on_submit():
            
            print("hi")

            review = Review(author=current_user, 
                            book=book, 
                            content=form.content.data)

            db.session.add(review)
            db.session.commit()

            return render_template('book.html', book=book, form=form)
        
    else:
        form = None
    
    return render_template('book.html', book=book, form=form)

## BOOK METHODS ##
@views.route('/finish-book', methods=['POST'])
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

@views.route('/start-book', methods=['POST'])
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

@views.route('/shelve-book', methods=['POST'])
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


@views.route('/wishlist-book', methods=['POST'])
@login_required
def wishlist_book():
    
    if request.method == 'POST':
        book_id = request.form.get('wish')
        book = Book.query.get_or_404(book_id)
        current_user.books_wish.append(book)
        db.session.commit()
    
        return render_template('/book.html', book=book, form=None)

# @views.route('/review-book', methods=['POST'])
# @login_required
# def review_book():
    
#     if request.method == 'POST':
        
#         book_id = request.form.get('review')
#         book = Book.query.get_or_404(book_id)
        





    #     book_id = request.form.get('start')
    #     ids_read = [book.id for book in current_user.books_read]
    #     ids_reading = [book.id for book in current_user.books_reading]
        
    #     if not book_in_lists(book_id, [ids_read, ids_reading]):
    #         print(f"book with id {book_id} not being read or already finished")
    #         book = Book.query.get_or_404(book_id)
    #         current_user.books_reading.append(book)
    #         db.session.commit()
            
    # return render_template('/book.html')
    # return redirect(url_for('views.home'))
    # return render_template('home.html', user=current_user)
















# @views.route('/search', methods=['GET'])
# @login_required
# def search(book_id):

#     return render_template('search.html', title=book.title, book=book)
# 

    # form = BookForm()
    # if form.validate_on_submit():
    #     book = Book(title=form.title.data, author=form.author.data, reader=current_user)
    #     db.session.add(book)
    #     db.session.commit()
    #     flash(f'{form.title.data} added to your reading list!', category='success')
    #     return redirect(url_for('views.home'))
    # return render_template('add_book.html', user=current_user, form=form)




# @views.route('/delete-note', methods=['POST'])
# def delete_note():
#     note = json.loads(request.data)
#     noteId = note['noteId']
#     note = Note.query.get(noteId)
#     if note:
#         if note.user_id == current_user.id:
#             db.session.delete(note)
#             db.session.commit()
    
#     return jsonify({})
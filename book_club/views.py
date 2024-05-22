from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from book_club import db
from book_club.models import Book, Review, User
from book_club.forms import BookForm, ReviewForm
from book_club.library import search_book

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

## USER PAGE ##
@views.route('/user/<int:user_id>', methods=['GET', 'POST'])
@login_required
def user(user_id):
    
    user = User.query.get_or_404(user_id)
    
    print(user)
    
    return render_template('user.html', user=user)

## MY LIBRARY PAGE ##
@views.route('/my-library', methods=['GET', 'POST'])
@login_required
def my_library():
    return render_template('user.html', user=current_user)

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
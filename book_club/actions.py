from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
import requests
from book_club import db
from book_club.models import Book, BookUserRel, Club, ClubUserRel
from book_club.genesis import create_club
from book_club.forms import ReviewForm, ClubJoinForm, ClubCreateForm
from book_club.aiapi import response_test
from book_club.library import search_book, search_by_olid, clean_description
from book_club.utils import BookStatusEnum

actions = Blueprint('actions', __name__)

## NEW CLUB ROUTE ##
@actions.route('/new-club', methods=['POST'])
@login_required
def new_club():
    
    form = ClubCreateForm()
    
    if form.validate_on_submit():
        
        club = Club.query.filter_by(name=form.name.data).first() 
        exists = bool(club)
        
        if exists is not True:
        
            new_club = create_club(form=form)
            new_club_rel = ClubUserRel(user=current_user, club=new_club)
            db.session.add(new_club_rel)
            db.session.commit()
            
            flash(f'{form.name.data} created!', category='success')
            return redirect(url_for('views.home'))
        
        else:
            
            flash(f'{club.name} name already taken', category='error')
   
## JOIN CLUB ROUTE ##
@actions.route('/join-club', methods=['POST'])
@login_required
def join_club():
    
    form = ClubJoinForm()
    
    if form.validate_on_submit():
        
        club = Club.query.filter_by(name=form.code.data).first() 
        exists = bool(club)
        
        if exists is True:
        
            new_club_rel = ClubUserRel(user=current_user, club=club)
            db.session.add(new_club_rel)
            
            flash(f'You joined {club.name}!', category='success')
            return redirect(url_for('views.home'))
        
        else:
            
            flash(f'{club.name} does not exist', category='error')
            

## WISHLIST BOOK ROUTE ##
@actions.route('/wishlist-book', methods=['POST'])
@login_required
def wishlist_book():
    
    if request.method == 'POST':
        book_id = request.form.get('wish')
        book = Book.query.get_or_404(book_id)
        
        current_user_relationship = BookUserRel.query.filter(BookUserRel.book==book, 
                                                        BookUserRel.user==current_user).first()

        if current_user_relationship is None:
            current_user_relationship = BookUserRel(user=current_user, book=book, status=BookStatusEnum.WISHLIST)
            db.session.add(current_user_relationship)
        else:
            current_user_relationship.status = BookStatusEnum.WISHLIST

        db.session.commit()
    
        return render_template('/book.html', book=book, form=None, relationship=current_user_relationship)
    
## START BOOK ROUTE ##
@actions.route('/start-book', methods=['POST'])
@login_required
def start_book():
    
    if request.method == 'POST':

        book_id = request.form.get('start')
        book = Book.query.get_or_404(book_id)
        
        current_user_relationship = BookUserRel.query.filter(BookUserRel.book==book, 
                                                        BookUserRel.user==current_user).first()

        if current_user_relationship is None:
            current_user_relationship = BookUserRel(user=current_user, book=book, status=BookStatusEnum.READING)
            db.session.add(current_user_relationship)
        else:
            current_user_relationship.status = BookStatusEnum.READING

        db.session.commit()
       
        db.session.commit()
    
        return render_template('book.html', book=book, form=None, relationship=current_user_relationship)

## FINISH BOOK ROUTE ##
@actions.route('/finish-book', methods=['POST'])
@login_required
def finish_book():
    
    if request.method == 'POST':
        
        book_id = request.form.get('finish')
        book = Book.query.get_or_404(book_id)
        
                
        current_user_relationship = BookUserRel.query.filter(BookUserRel.book==book, 
                                                        BookUserRel.user==current_user).first()

        if current_user_relationship is None:
            current_user_relationship = BookUserRel(user=current_user, book=book, status=BookStatusEnum.FINISHED)
            db.session.add(current_user_relationship)
        else:
            current_user_relationship.status = BookStatusEnum.FINISHED

        db.session.commit()
        
        form = ReviewForm()

        return redirect(url_for('views.book'))

## SHELVE BOOK ROUTE ##
@actions.route('/shelve-book', methods=['POST'])
@login_required
def shelve_book():
    
    if request.method == 'POST':
        
        book_id = request.form.get('shelve')
        book = Book.query.get_or_404(book_id)
        
                
        current_user_relationship = BookUserRel.query.filter(BookUserRel.book==book, 
                                                        BookUserRel.user==current_user).first()

        if current_user_relationship is not None:
            db.session.delete(current_user_relationship)
            
        db.session.commit()

        return redirect(url_for('views.book'))
    
## FAVOURITE BOOK ROUTE ##
@actions.route('/favourite-book', methods=['POST'])
@login_required
def favourite_book():
    
    if request.method == 'POST':
        
        book_id = request.form.get('favourite')
        book = Book.query.get_or_404(book_id)
        
                
        current_user_relationship = BookUserRel.query.filter(BookUserRel.book==book, 
                                                        BookUserRel.user==current_user).first()

        if current_user_relationship is not None:
            old_favourite_status = current_user_relationship.favourite
            current_user_relationship.favourite = not old_favourite_status
            
        db.session.commit()

        return redirect(url_for('views.book', book=book))

## FIND BOOK ROUTE ##
@actions.route('/find-book', methods=['POST'])
@login_required
def find_book():
    
    if request.method == 'POST':
        
        rec_info = request.form.get('rec')
        rec_title = rec_info[0]
        rec_author = rec_info[1]
        
        _ = search_book(rec_title, rec_author)
        
        
## ADD BOOK ROUTE ##
@actions.route('/add-book', methods=['GET', 'POST'])
@login_required
def add_book():
    
    if request.method == 'POST':
        
        olid = request.form.get('add')
        
        book = Book.query.filter_by(olid=olid).first()
        exists = bool(book)
        
        if exists is not True:
        
            book_info = search_by_olid(olid)
            book = Book(title=book_info["title"], 
                        author=book_info["author"], 
                        olid=book_info["olid"],
                        description=clean_description(book_info["description"]),
                        cover_url=book_info["cover_url"])

            db.session.add(book)
            flash(f'{book_info["title"]} added to book club!', category='success')

        db.session.commit()

        return render_template('book.html', book=book, form=None, current_user_relationship=None)

## GPT RECCOMEND ROUTE ##
@actions.route('/gpt-reccomend', methods=['POST'])
@login_required
def gpt_reccomend():
    
    if request.method == 'POST':
        
        response = response_test()
    
    return render_template('reccomend.html', user=current_user, response=response)

## API TEST ROUTE ##
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

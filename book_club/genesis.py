import random
import string

from flask_login import current_user

from book_club.models import User, Club
from book_club import db, bcrypt

def create_user(form):
    hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
    new_user = User(email=form.email.data, 
                    username=form.username.data, 
                    password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    
def create_club(form):
    
    join_code = join_code_generator()
    size_books = len(current_user.books)
    # admin
    
    new_club = Club(name=form.name.data,
                    join_code=join_code,
                    users=current_user,
                    size_users=1,
                    size_books=size_books)
    
    print(new_club)
    
    db.session.add(new_club)
    db.session.commit()
    
    return new_club
    
def join_code_generator():
    n = 5
    chars = string.ascii_uppercase + string.digits
    join_code = ''.join(random.choice(chars) for _ in range(n))
    return join_code
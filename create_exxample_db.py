from os import path
import lorem
import random
import json
import statistics

from book_club import app, db, bcrypt, DB_NAME
from book_club.models import User, Book, BookUserRel, Article
from book_club.utils import BookStatusEnum, ArticleTypeEnum

def run():
    if not path.exists('flask_web/' + DB_NAME):
        with app.app_context():
            db.create_all()
        
        load_dummy_data(print_db=True)

def dummy_articles(users):
    
    images = ["/static/images/article_images/randim_"+str(i)+".jpg" for i in range(1,11)]
    type = random.choice(list(ArticleTypeEnum))
    
    articles = [Article(title=lorem.sentence(),
                        type=type,
                        content=lorem.text(),
                        images = json.dumps([images[i]]),
                        thumbnail = images[i],
                        user=users[i]) for i in range(0,5)]
    
    return articles

def dummy_users():
    
    user_hashed_password = bcrypt.generate_password_hash("ciao").decode('utf-8')
    usernames = import_username_json()
    
    users = [User(email=username["username"]+"@example.com", 
                    username=username["username"], 
                    password=user_hashed_password) for username in usernames]
    
    return users

def admin_user():
    
    admin_hashed_password = bcrypt.generate_password_hash("yatch").decode('utf-8')
    admin = User(email="admin@example.com", 
                    username="admin", 
                    password=admin_hashed_password)
    
    return admin
    
def add_users():
    
    users = dummy_users()
    users.append(admin_user())

    return users
        
def import_book_json(json_name):
    
    with open('json/'+json_name, 'r') as f:
        data = json.loads(f.read())
        
        return data
    
def import_username_json():
    
    with open('json/names.json', 'r') as f:
        data = json.loads(f.read())
        
        return data

def add_relationship_random(user, book):
    
    status = random.choices(
        list(BookStatusEnum), cum_weights=(5, 25, 100))[0]
    relationship = BookUserRel(user=user, book=book, status=status)
    
    if status.name == "FINISHED":
        relationship.review=lorem.paragraph()
        relationship.rating=random.choice([0.5, 1.0, 1.5, 2.0, 2.5, 3.0])
        
        favourite = random.randrange(0,1)
        
        if favourite < 0.15:
            relationship.favourite = True
        
    db.session.add(relationship)

def load_book_data():
    
    books_api_info = import_book_json("book-data.json")
    
    books = [Book(title=book_info["title"], 
                author=book_info["author"], 
                olid=book_info["olid"],
                description=book_info["description"],
                cover_url=book_info["cover_url"]) for book_info in books_api_info]
    
    return books

def load_dummy_data(print_db=False):
    
    n_books_per_user = 25
    
    with app.app_context():
    
        users = add_users()
        
        [db.session.add(user) for user in users]
        
        books = load_book_data()
        
        [db.session.add(book) for book in books]
        
        for user in users:
            for i in random.sample(range(0, 81), n_books_per_user):
                add_relationship_random(user, books[i])

        db.session.commit()
        
        average_ratings()
        articles = dummy_articles(users)
        [db.session.add(article) for article in articles]
        
        db.session.commit()
        
        if print_db:
            
            print("Users ----------")
            [print(user) for user in users]
            
            print("Books ----------")
            [print(book) for book in books]
            

def average_ratings():
    
    books = Book.query.all()

    for book in books:
        
        relationships = [relationship for relationship in book.user_relationships if relationship.status == BookStatusEnum.FINISHED]

        ratings =  [relationship.rating for relationship in relationships]
        
        if len(ratings) != 0:
        
            avg_rating = statistics.mean(ratings)

            book.average_rating = avg_rating

    
if __name__ == "__main__":    
    run()
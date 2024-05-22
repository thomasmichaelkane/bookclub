from os import path
import lorem

from book_club import app, db, bcrypt, DB_NAME
from book_club.models import User, Book, Review
from book_club.retr import search_book

def create_database():
    if not path.exists('flask_web/' + DB_NAME):
        with app.app_context():
            db.create_all()
            
        add_dummy()
        
def add_books():
    
    books_api_info = []
    
    books_api_info.append(search_book("Oliver Twist", "Charles Dickens"))
    books_api_info.append(search_book("My Life", "Anton Chekhov"))
    books_api_info.append(search_book("MacBeth", "William Shakespeare"))
    books_api_info.append(search_book("Beautiful Star", "Yukio Mishima"))
    books_api_info.append(search_book("The Lord of the Rings", "J.R.R. Tolkien"))
    books_api_info.append(search_book("1984", "George Orwell"))
    books_api_info.append(search_book("To Kill a Mockingbird", "Harper Lee"))
    books_api_info.append(search_book("Pride and Prejudice", "Jane Austen"))
    books_api_info.append(search_book("The Great Gatsby", "F. Scott Fitzgerald"))
    books_api_info.append(search_book("The Catcher in the Rye", "J.D. Salinger"))
    books_api_info.append(search_book("Moby-Dick", "Herman Melville"))
    books_api_info.append(search_book("The Hobbit", "J.R.R. Tolkien"))
    books_api_info.append(search_book("Brave New World", "Aldous Huxley"))
    books_api_info.append(search_book("The Hitchhiker's Guide to the Galaxy", "Douglas Adams"))
    books_api_info.append(search_book("Harry Potter and the Sorcerer's Stone", "J.K. Rowling"))
    books_api_info.append(search_book("The Da Vinci Code", "Dan Brown"))
    books_api_info.append(search_book("Frankenstein", "Mary Shelley"))
    books_api_info.append(search_book("The Hunger Games", "Suzanne Collins"))
    books_api_info.append(search_book("The Adventures of Sherlock Holmes", "Arthur Conan Doyle"))
    books_api_info.append(search_book("The Chronicles of Narnia: The Lion, the Witch and the Wardrobe", "C.S. Lewis"))
    books_api_info.append(search_book("The Alchemist", "Paulo Coelho"))
    books_api_info.append(search_book("Gone with the Wind", "Margaret Mitchell"))
    books_api_info.append(search_book("The Picture of Dorian Gray", "Oscar Wilde"))
    books_api_info.append(search_book("Lord of the Flies", "William Golding"))
    books_api_info.append(search_book("Wuthering Heights", "Emily Brontë"))

    books = [Book(title=book_info["title"], 
                  author=book_info["author"], 
                  olid=book_info["olid"],
                  cover_url_s=book_info["cover_url_s"], 
                  cover_url_m=book_info["cover_url_m"],
                  cover_url_l=book_info["cover_url_l"]) for book_info in books_api_info]
    
    print(books)
    
    return books

def add_review(user, book):
    
    review = Review(content=lorem.paragraph(), author=user, book=book)
    db.session.add(review)
            
def add_dummy():
    
    with app.app_context():
    
        admin_hashed_password = bcrypt.generate_password_hash("yatch").decode('utf-8')
        dummy_hashed_password = bcrypt.generate_password_hash("ciao").decode('utf-8')
        
        users=[User(email="admin@example.com", 
                        username="admin", 
                        password=admin_hashed_password),
        User(email="dummy1@example.com", 
                        username="dummy1", 
                        password=dummy_hashed_password),
        User(email="dummy2@example.com", 
                        username="dummy2", 
                        password=dummy_hashed_password),
        User(email="dummy3@example.com", 
                        username="dummy3", 
                        password=dummy_hashed_password),
        User(email="dummy4@example.com", 
                        username="dummy4", 
                        password=dummy_hashed_password)]
        

        
        for user in users:
            db.session.add(user)
        
        books = add_books()
        
        for book in books:
            db.session.add(book)
        
        for i in range(1,15):
            users[0].books_read.append(books[i])
            if i < 10:
                add_review(users[0], books[i])
        users[0].books_reading.append(books[0])
        
        for i in range(4,9):
            users[1].books_read.append(books[i])
            add_review(users[1], books[i])
        users[1].books_reading.append(books[3])
        
        for i in range(15,20):
            users[2].books_read.append(books[i])
            add_review(users[2], books[i])
        users[2].books_reading.append(books[12])
        
        for i in range(5,9):
            users[3].books_read.append(books[i])
            add_review(users[3], books[i])
        users[3].books_reading.append(books[0])
        users[3].books_reading.append(books[18])
        
        for i in range(13,17):
            users[4].books_read.append(books[i])
            add_review(users[4], books[i])
        
        db.session.commit()
        
create_database()
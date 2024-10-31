import json
from book_club.library import search_book, search_by_olid

def run():
    
    books_api_info = import_book_titles_json("book-data-raw.json")
    
    books_info_from_olid = [search_by_olid(book["olid"]) for book in books_api_info] 
    
    save_book_json(books_info_from_olid, "book-data.json")

def get_books_api_info(books_info):
    
    return [search_book(book["title"], book["author"]) for book in books_info]

def import_book_titles_json(json_name):
    
    with open('json/'+json_name, 'r') as f:
        books_info = json.loads(f.read())
        
        return books_info
    
def save_book_json(data, json_name):
    
    with open('json/'+json_name, 'w') as f:
        json.dump(data, f)
        
if __name__ == '__main__':
    run()
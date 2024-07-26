import requests
import random

def book_in_lists(book_id, lists):
    
    book_id_int = int(book_id)
    
    for list in lists:
        if book_id_int in list:
            return True
    
    # else
    return False

def get_cover_url(cover_id):
    
    url =  f"https://covers.openlibrary.org/b/id/{cover_id}-L.jpg"
    
    return url

def get_olid_from_str(olid_str):
    
    return olid_str.strip("/works/")

def get_author_key_from_str(author_key_str):
    
    return author_key_str.strip("/authors/")

def response_with_catch(url):
    
    response = requests.get(url)
    response.raise_for_status()  # raises exception when not a 2xx response
    if response.status_code != 204:
        return response.json()

def search_by_olid(olid):
    
    api_search = "https://openlibrary.org/works/" + str(olid) + ".json"
    api_response = response_with_catch(api_search)

    book_info = get_book_info_olid(api_response)
    
    return book_info

def search_author_by_key(author_key):
    
    api_search = "https://openlibrary.org/authors/" + str(author_key) + ".json"
    api_response = response_with_catch(api_search)
    
    return api_response

def search_book(title, author, n=1):
    
    title_search = "title=" + title.strip(" ").replace(" ", "+")
    
    if author != "":
        author_search = "author=" + author.strip(" ").replace(" ", "+")
        api_search = "https://openlibrary.org/search.json?" + title_search + "&" + author_search
    else:
        api_search = "https://openlibrary.org/search.json?" + title_search

    api_response = response_with_catch(api_search)
    
    if len(api_response["docs"]) != 0:
        if n == 1:
            book_info = get_book_info(api_response["docs"][0])
        else:
            book_info = [get_book_info(api_response["docs"][i]) for i in range(0,n)]
        
    else:
        book_info = None
    
    return book_info

def clean_description(old_description):
    
    if old_description is not None:
        breaker_line = old_description.find("--------")
        
        new_description = old_description[0:breaker_line]
        
        return new_description
    
    else:
        
        return old_description

def get_book_info_olid(result):
    
    title = result["title"]
    author_str = result["authors"][0]["author"]["key"]
    
    author_key = get_author_key_from_str(author_str)
    author_result = search_author_by_key(author_key)
    
    author = author_result["name"]
    olid = get_olid_from_str(result["key"])
    
    try:
        description = result["description"]
        print(len(description))
        if isinstance(description, dict):
            description = description["value"]
            
        description = clean_description(description)
            
    except KeyError:
        description = None
    
    try:
        cover_id = result["covers"][0]
        if float(cover_id) < 100:
            cover_id = result["covers"][1]
        
        cover_url = get_cover_url(cover_id)
    except KeyError:
        cover_url = "/static/images/cover-blank.png"
        
    book_info = {"title": title, 
                "author": author,
                "olid": olid,
                "description": description ,
                "cover_url": cover_url}
    
    return book_info

def get_book_info(result):
        
    title = result["title"]
    author = result["author_name"][0]
    olid = get_olid_from_str(result["key"])
    
    try:
        cover_id = result["cover_i"]
        cover_url = get_cover_url(cover_id)
    except KeyError:
        cover_url = "/static/images/cover-blank.png"
    
    book_info = {"title": title, 
                "author": author,
                "olid": olid,
                "cover_url": cover_url}
    
    return book_info

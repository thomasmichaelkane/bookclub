import requests
import random

def random_book_color():
    
    palette = ["#D7E2DC", "#F8EDEB", "#FAE1DD", "#DED5CE", "#FEC5BA", "#F5EBE1"]
        
    return random.choice(palette)

def book_in_lists(book_id, lists):
    
    book_id_int = int(book_id)
    
    for list in lists:
        if book_id_int in list:
            return True
    
    # else
    return False

def get_cover_urls(cover_id):
    
    img_s =  f"https://covers.openlibrary.org/b/id/{cover_id}-S.jpg"
    img_m =  f"https://covers.openlibrary.org/b/id/{cover_id}-M.jpg"
    img_l =  f"https://covers.openlibrary.org/b/id/{cover_id}-L.jpg"
    
    return img_s, img_m, img_l

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
    
    print(api_response)

    book_info = get_book_info_olid(api_response)
    
    print(book_info)
    
    return book_info

def search_author_by_key(author_key):
    
    api_search = "https://openlibrary.org/authors/" + str(author_key) + ".json"
    api_response = response_with_catch(api_search)
    
    return api_response

def search_book(title, author):
    
    title_search = "title=" + title.strip(" ").replace(" ", "+")
    
    if author != "":
        author_search = "author=" + author.strip(" ").replace(" ", "+")
        api_search = "https://openlibrary.org/search.json?" + title_search + "&" + author_search
    else:
        api_search = "https://openlibrary.org/search.json?" + title_search

    api_response = response_with_catch(api_search)
    
    if len(api_response["docs"]) != 0:
        book_info = get_book_info(api_response["docs"][0])
        
    else:
        book_info = None
    
    print(book_info)
    
    return book_info

def get_book_info_olid(result):
    
    title = result["title"]
    author_str = result["authors"][0]["author"]["key"]
    
    author_key = get_author_key_from_str(author_str)
    author_result = search_author_by_key(author_key)
    
    author = author_result["name"]
    olid = get_olid_from_str(result["key"])
    
    try:
        cover_id = result["cover_i"]
    except KeyError:
        cover_id = "14586152"
        
    cover_url_s, cover_url_m, cover_url_l = get_cover_urls(cover_id)
    
    book_info = {"title": title, 
                "author": author,
                "olid": olid,
                "cover_url_s": cover_url_s, 
                "cover_url_m": cover_url_m, 
                "cover_url_l": cover_url_l}
    
    return book_info

def get_book_info(result):
        
    title = result["title"]
    author = result["author_name"][0]
    olid = get_olid_from_str(result["key"])
    
    try:
        cover_id = result["cover_i"]
    except KeyError:
        cover_id = "14586152"
        
    cover_url_s, cover_url_m, cover_url_l = get_cover_urls(cover_id)
    
    book_info = {"title": title, 
                "author": author,
                "olid": olid,
                "cover_url_s": cover_url_s, 
                "cover_url_m": cover_url_m, 
                "cover_url_l": cover_url_l}
    
    return book_info

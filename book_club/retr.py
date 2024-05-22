import requests
from flask import Blueprint

retr = Blueprint('retr', __name__)

@retr.route('/lotr_test', methods=['GET', 'POST'])
def lotr_test():
    
    api_response = requests.get('https://openlibrary.org/search.json?title=the+lord+of+the+rings').json()
    
    lotr = api_response["docs"][0]
    
    title = lotr["title"]
    author = lotr["author_name"]
    cover_id = lotr["cover_i"]
    img_url = f"https://covers.openlibrary.org/b/id/{cover_id}-M.jpg"
    
    print(title, author, img_url)
    
    # for i, (key, value) in enumerate(lotr.items()):
    #     print(key, ":", value) 
        
    #     if i == 2:
    #         break
        
    
    return lotr

def get_cover_urls(cover_id):
    
    img_s =  f"https://covers.openlibrary.org/b/id/{cover_id}-S.jpg"
    img_m =  f"https://covers.openlibrary.org/b/id/{cover_id}-M.jpg"
    img_l =  f"https://covers.openlibrary.org/b/id/{cover_id}-L.jpg"
    
    return img_s, img_m, img_l
    

def get_olid_from_str(olid_str):
    
    return olid_str.strip("/works/")

def response_with_catch(url):
    
    response = requests.get(url)
    response.raise_for_status()  # raises exception when not a 2xx response
    if response.status_code != 204:
        return response.json()


def search_book(title, author):
    
    title_search = "title=" + title.strip(" ").replace(" ", "+")
    
    if author != "":
        author_search = "author=" + author.strip(" ").replace(" ", "+")
        api_search = "https://openlibrary.org/search.json?" + title_search + "&" + author_search
    else:
        api_search = "https://openlibrary.org/search.json?" + title_search

    print(api_search)
    
    api_response = response_with_catch(api_search)
    
    if len(api_response["docs"]) != 0:
    
        first_result = api_response["docs"][0]
        
        title = first_result["title"]
        author = first_result["author_name"][0]
        olid = get_olid_from_str(first_result["key"])
        
        try:
            cover_id = first_result["cover_i"]
        except KeyError:
            cover_id = "14586152"
            
        cover_url_s, cover_url_m, cover_url_l = get_cover_urls(cover_id)
        
        book_info = {"title": title, 
                    "author": author,
                    "olid": olid,
                    "cover_url_s": cover_url_s, 
                    "cover_url_m": cover_url_m, 
                    "cover_url_l": cover_url_l}
        
    else:
        
        book_info = None
    
    print(book_info)
    
    return book_info


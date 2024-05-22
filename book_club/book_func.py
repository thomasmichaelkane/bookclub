import random

def book_in_lists(book_id, lists):
    
    book_id_int = int(book_id)
    
    for list in lists:
        if book_id_int in list:
            return True
    
    # else
    return False
        
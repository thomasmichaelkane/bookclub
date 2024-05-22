import random
# from jinja2 import FileSystemLoader, Environment
 
# loader = FileSystemLoader('/templates')


    
# environment = Environment(autoescape=True, loader=loader)
# environment.filters['shuffle'] = filter_shuffle

def random_book_color():
    
    palette = ["#D7E2DC", "#F8EDEB", "#FAE1DD", "#DED5CE", "#FEC5BA", "#F5EBE1"]
        
    return random.choice(palette)

from flask_login import current_user
from book_club.library import search_book
from openai import OpenAI
import re

def create_by_reading_prompt():
    
    books = []
    
    for book in current_user.books_reading:
        book_str = f'"{book.title}" by "{book.author}"'
        books.append(book_str)
        
    prompt = ("Can you recommend me three books based on the list of "
    "books that I'm currently reading. The books I'm currently read are: "
    + (", ".join(books)) + ".")
    
    print(prompt)
    
def gpt_test():
   
    client = OpenAI(api_key="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")
   
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": "Say this is a test"}
        ]
    )
    
    print(response)
    
def rec_test():
        
    client = OpenAI(api_key="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")
   
    example_prompt = 'Can you recommend me three books based on the list of books that I\'m currently reading. The books I\'m currently read are: "1984" by "george orwell", "on the road" by "jack kerouac". In your response can you wrap each section in an appropriate tag, for example <intro>, <title>, <author>, <description>, and <outro>.'
    
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": example_prompt}
        ]
    )
    
    # print(response.choices[0].message.content)
    
def openai_recomend(prompt):
   
    client = OpenAI(api_key="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")
   
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    
    print(response)
    
def response_test():
    
    response = example_response()
    
    response_data = extract_response_data(response)
    
    print(response_data)
    
    return response_data
    
def example_response():
    
    response = '<intro>\nBased on the books you\'re currently reading, I recommend the following three books:\n</intro>\n\n<title>\n"The Catcher in the Rye"\n</title>\n<author>\nby J.D. Salinger\n</author>\n<description>\nThis classic novel follows the story of Holden Caulfield as he navigates the challenges of adolescence and the complexities of growing up. Much like "On the Road," this book delves into themes of rebellion and the search for meaning in a conformist society.\n</description>\n\n<title>\n"Brave New World"\n</title>\n<author>\nby Aldous Huxley\n</author>\n<description>\nIn this dystopian novel, Huxley explores a world where technology, consumerism, and social conditioning reign supreme. Much like "1984," this book offers a thought-provoking look at the dangers of a totalitarian regime and the loss of individuality.\n</description>\n\n<title>\n"Fear and Loathing in Las Vegas"\n</title>\n<author>\nby Hunter S. Thompson\n</author>\n<description>\nThis gonzo journalism classic follows the wild and drug-fueled adventures of Raoul Duke and his attorney, Dr. Gonzo, as they journey through Las Vegas. Like "On the Road," this book captures the spirit of rebellion and the quest for authenticity in a world of artificiality.\n</description>\n\n<outro>\nI hope you enjoy these book recommendations based on your current reading list!\n</outro>'

    return response

def extract_response_data(response):
    
    recs = []
    
    intro = find_tagged_sections("intro", response)[0]
    intro = intro.removeprefix('\n').removesuffix('\n').strip('"')
    
    outro = find_tagged_sections("outro", response)[0]
    outro = outro.removeprefix('\n').removesuffix('\n').strip('"')
    
    titles = find_tagged_sections("title", response)
    titles = [title.removeprefix('\n').removesuffix('\n').strip('"') for title in titles]
    
    authors = find_tagged_sections("author", response)
    authors = [author.removeprefix('\n').removesuffix('\n').removeprefix('by ') for author in authors]
    
    descriptions = find_tagged_sections("description", response)
    descriptions = [description.removeprefix('\n').removesuffix('\n') for description in descriptions]

    for i in range(len(titles)):

        openlib_api_info = search_book(titles[i], authors[i])
        
        found = True if openlib_api_info is not None else False
        
        rec = {"title": titles[i], "author": authors[i], "description": descriptions[i], "openlib_found": found, "openlib_api_info": openlib_api_info} 
        recs.append(rec)
        
    return intro, outro, recs

def find_tagged_sections(name, string):
    
    start_tag = "<" + name + ">"
    end_tag = "</" + name + ">"
    
    print(start_tag)

    sec_start = [t.start() + len(start_tag) for t in re.finditer(start_tag, string)]
    sec_end = [t.start() for t in re.finditer(end_tag, string)]
    
    sec_indices = list(zip(sec_start, sec_end))
    
    print(sec_indices)
    
    sections =  [string[s:e] for (s, e) in sec_indices]
    
    return sections
        
        
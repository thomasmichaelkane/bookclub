from enum import Enum
import random

class BookStatusEnum(Enum):
    WISHLIST = 1
    READING = 2
    FINISHED = 3
    
class ArticleTypeEnum(Enum):
    BOOK = 1
    AUTHOR = 2
    GENERAL = 3
    
def get_iterables_dict(seq):
    iter_dict = {key: iter(item) for key, item in seq.items()}
    return iter_dict

def band_generator(dict):
    
    weights = [0.3, 0.6, 0.1]
    
    key = random.choices(list(dict.keys()), weights=weights)[0]
    
    try:
        x = next(dict[key])
        yield key, x
    
    except StopIteration:
        yield None, None
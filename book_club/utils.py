from enum import Enum

class BookStatusEnum(Enum):
    WISHLIST = 1
    READING = 2
    FINISHED = 3
    
class ArticleTypeEnum(Enum):
    BOOK = 1
    AUTHOR = 2
    GENERAL = 3
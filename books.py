from fastapi import FastAPI, Body

app = FastAPI()

BOOKS = [
    {'title': 'A Brief History of Time', 'author': 'Stephen Hawking', 'category': 'science'},
    {'title': 'The Selfish Gene', 'author': 'Richard Dawkins', 'category': 'science'},
    {'title': 'Sapiens: A Brief History of Humankind', 'author': 'Yuval Noah Harari', 'category': 'history'},
    {'title': 'A People’s History of the United States', 'author': 'Howard Zinn', 'category': 'history'},
    {'title': 'The Man Who Knew Infinity', 'author': 'Robert Kanigel', 'category': 'math'},
    {'title': 'Fermat’s Enigma', 'author': 'Simon Singh', 'category': 'math'}
]

# * get methods

@app.get('/books')
async def read_all_books():
    return BOOKS

@app.get("/books/{book_author}/")
async def read_author_category_by_query(book_author: str, category: str):
    books_to_return = []
    for book in BOOKS:
        if book.get('author').casefold() == book_author.casefold() and \
            book.get('category').casefold() == category.casefold():
                books_to_return.append(book)
    return books_to_return

# * post methods

@app.post('/books/createbooks')
async def create_books(books: list):
    for book in books:
        BOOKS.append(book)
    return books
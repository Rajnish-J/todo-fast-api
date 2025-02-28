# * Importing necessary libraries

from fastapi import FastAPI, Body, HTTPException
from pydantic import BaseModel
from typing import List, Optional

# * Create a FastAPI instance

app = FastAPI()

class Book:
    id: int
    title: str
    author: str
    description: Optional[str] = None
    category: str
    rating: int
    
    def __init__(self, id, title, author, description, category, rating):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.category = category
        self.rating = rating

# * Sample book data
BOOKS = [
    Book(1, 'A Brief History of Time', 'Stephen Hawking', 'A Brief History of Time is a popular-science book by Stephen Hawking', 'science', 5),
    Book(2, 'The Selfish Gene', 'Richard Dawkins', 'The Selfish Gene is a 1976 book on evolution by Richard Dawkins', 'science', 4),
    Book(3, 'Sapiens: A Brief History of Humankind', 'Yuval Noah Harari', 'Sapiens: A Brief History of Humankind is a book by Yuval Noah Harari', 'history', 4),
    Book(4, 'A People’s History of the United States', 'Howard Zinn', 'A People’s History of the United States is a book by Howard Zinn', 'history', 3),
    Book(5, 'The Da Vinci Code', 'Dan Brown', 'The Da Vinci Code is a 2003 mystery thriller novel by Dan Brown', 'thriller', 4),
    Book(6, 'The Alchemist', 'Paulo Coelho', 'The Alchemist is a novel by Brazilian author Paulo Coelho', 'fiction', 5)
]

# * Define a Pydantic model for book validation
class Book(BaseModel):
    title: str
    author: str
    category: str

# * GET Methods

@app.get('/books')
async def read_all_books():
    return BOOKS

@app.get('/books/{book_title}')
async def read_book(book_title: str):
    for book in BOOKS:
        if book.get('title').casefold() == book_title.casefold():
            return book
    raise HTTPException(status_code=404, detail="Book not found")

@app.get('/books/')
async def read_category_by_query(category: str):
    books_to_return = [book for book in BOOKS if book.get('category').casefold() == category.casefold()]
    if not books_to_return:
        raise HTTPException(status_code=404, detail="No books found in this category")
    return books_to_return

@app.get('/books/{book_author}/')
async def read_author_category_by_query(book_author: str, category: str):
    books_to_return = [
        book for book in BOOKS if book.get('author').casefold() == book_author.casefold() and 
        book.get('category').casefold() == category.casefold()
    ]
    if not books_to_return:
        raise HTTPException(status_code=404, detail="No books found for this author in the given category")
    return books_to_return

# * POST Method (Create a book)

@app.post('/books/createbooks')
async def create_books(book: Book):
    # Check if book already exists
    for existing_book in BOOKS:
        if existing_book['title'].casefold() == book.title.casefold():
            raise HTTPException(status_code=400, detail="Book already exists")
    
    BOOKS.append(book.dict())  # Convert Pydantic object to dictionary
    return {"message": "Book added successfully", "book": book}

# * PUT Method (Update a book)

@app.put('/books/{book_title}')
async def update_book(book_title: str, updated_book: Book):
    for index, book in enumerate(BOOKS):
        if book.get('title').casefold() == book_title.casefold():
            BOOKS[index] = updated_book.dict()
            return {"message": "Book updated successfully", "book": updated_book}
    
    raise HTTPException(status_code=404, detail="Book not found")

# * DELETE Method (Delete a book)

@app.delete('/books/{book_title}')
async def delete_book(book_title: str):
    for i in range(len(BOOKS)):
        if BOOKS[i].get('title').casefold() == book_title.casefold():
            BOOKS.pop()
            return {"message": "Book deleted successfully"}
    return {"message": "Book not found"}
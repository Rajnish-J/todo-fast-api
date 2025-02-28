# * Importing necessary libraries

from fastapi import FastAPI, Body, HTTPException
from pydantic import BaseModel
from typing import List, Optional

# * Create a FastAPI instance

app = FastAPI()

class Book(BaseModel):
    id: int
    title: str
    author: str
    description: Optional[str] = None
    category: str
    rating: int


# * Sample book data
BOOKS: List[Book] = [
    Book(id=1, title='A Brief History of Time', author='Stephen Hawking',
         description='A popular-science book by Stephen Hawking', category='science', rating=5),
    Book(id=2, title='The Selfish Gene', author='Richard Dawkins',
         description='A book on evolution by Richard Dawkins', category='science', rating=4),
    Book(id=3, title='Sapiens: A Brief History of Humankind', author='Yuval Noah Harari',
         description='A book by Yuval Noah Harari', category='history', rating=4),
    Book(id=4, title='A People’s History of the United States', author='Howard Zinn',
         description='A book by Howard Zinn', category='history', rating=3),
    Book(id=5, title='The Da Vinci Code', author='Dan Brown',
         description='A mystery thriller novel by Dan Brown', category='thriller', rating=4),
    Book(id=6, title='The Alchemist', author='Paulo Coelho',
         description='A novel by Brazilian author Paulo Coelho', category='fiction', rating=5)
]



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

# ! ---------------------------- END OF CODE Project 1 API ---------------------------- !


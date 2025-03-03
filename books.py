# * Import necessary libraries
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional

# * Create a FastAPI instance
app = FastAPI()

# * Convert `Book` into a Pydantic model
class Book(BaseModel):
    id: int
    title: str = Field(min_length=2, max_length=80)
    author: str = Field(min_length=2, max_length=40)
    description: Optional[str] = Field(None, min_length=2, max_length=200)
    category: str = Field(min_length=2, max_length=40)
    rating: int = Field(..., ge=1, le=5)

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

# * creating a function to generate a new id for the book
def generate_book_id(BOOKS):
    if BOOKS:
        return BOOKS[-1].id + 1
    return 1

# * GET Methods
@app.get('/books', response_model=List[Book])
async def read_all_books():
    return BOOKS

@app.get('/books/{book_title}', response_model=Book)
async def read_book(book_title: str):
    for book in BOOKS:
        if book.title.casefold() == book_title.casefold():
            return book
    raise HTTPException(status_code=404, detail="Book not found")

@app.get('/books/', response_model=List[Book])
async def read_category_by_query(category: str):
    books_to_return = [book for book in BOOKS if book.category.casefold() == category.casefold()]
    if not books_to_return:
        raise HTTPException(status_code=404, detail="No books found in this category")
    return books_to_return

@app.get('/books/{book_author}/', response_model=List[Book])
async def read_author_category_by_query(book_author: str, category: str):
    books_to_return = [
        book for book in BOOKS if book.author.casefold() == book_author.casefold() and 
        book.category.casefold() == category.casefold()
    ]
    if not books_to_return:
        raise HTTPException(status_code=404, detail="No books found for this author in the given category")
    return books_to_return

# * POST Method (Create a book)
@app.post('/books/createbooks', response_model=Book)
async def create_books(book: Book):
    # Check if book already exists
    for existing_book in BOOKS:
        if existing_book.title.casefold() == book.title.casefold():
            raise HTTPException(status_code=400, detail="Book already exists")
    
    BOOKS.append(book)
    return book

# * PUT Method (Update a book)
@app.put('/books/{book_title}', response_model=Book)
async def update_book(book_title: str, updated_book: Book):
    for index, book in enumerate(BOOKS):
        if book.title.casefold() == book_title.casefold():
            BOOKS[index] = updated_book
            return updated_book
    
    raise HTTPException(status_code=404, detail="Book not found")

# * DELETE Method (Delete a book)
@app.delete('/books/{book_title}', response_model=dict)
async def delete_book(book_title: str):
    for i, book in enumerate(BOOKS):
        if book.title.casefold() == book_title.casefold():
            BOOKS.pop(i)
            return {"message": "Book deleted successfully"}
    
    raise HTTPException(status_code=404, detail="Book not found")

# ! ---------------------------- END OF CODE Project 1 API ---------------------------- !

# * Endpoint to create book with BookRequest validation
class BookRequest(BaseModel):
    id: int
    title: str = Field(min_length=2, max_length=80)
    author: str = Field(min_length=2, max_length=40)
    description: str = Field(min_length=2, max_length=200)
    category: str = Field(min_length=2, max_length=40)
    rating: int = Field(..., ge=1, le=5)


@app.post("/bookObj/create_book/", response_model=Book)
async def create_book(Book_request: BookRequest):
    new_book = Book(**Book_request.model_dump())  # Convert Pydantic object to dictionary
    new_book.id = generate_book_id(BOOKS)
    BOOKS.append(new_book)
    return new_book


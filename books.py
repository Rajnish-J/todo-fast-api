from fastapi import FastAPI, HTTPException, Path, status
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

# * Function to generate a new ID for the book
def generate_book_id(BOOKS):
    return (BOOKS[-1].id + 1) if BOOKS else 1

# * GET Methods
@app.get('/books', response_model=List[Book], status_code=status.HTTP_200_OK)
async def read_all_books():
    if not BOOKS:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No books available")
    return BOOKS

@app.get('/books/{book_title}', response_model=Book, status_code=status.HTTP_200_OK)
async def read_book(book_title: str):
    for book in BOOKS:
        if book.title.casefold() == book_title.casefold():
            return book
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")

@app.get('/books/', response_model=List[Book], status_code=status.HTTP_200_OK)
async def read_category_by_query(category: str):
    books_to_return = [book for book in BOOKS if book.category.casefold() == category.casefold()]
    if not books_to_return:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No books found in this category")
    return books_to_return

@app.get('/books/{book_author}/', response_model=List[Book], status_code=status.HTTP_200_OK)
async def read_author_category_by_query(book_author: str, category: str):
    books_to_return = [
        book for book in BOOKS if book.author.casefold() == book_author.casefold() and 
        book.category.casefold() == category.casefold()
    ]
    if not books_to_return:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No books found for this author in the given category")
    return books_to_return

# * POST Method (Create a book)
@app.post('/books/createbooks', response_model=Book, status_code=status.HTTP_201_CREATED)
async def create_books(book: Book):
    # Check if book already exists
    for existing_book in BOOKS:
        if existing_book.title.casefold() == book.title.casefold():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Book already exists")
    
    BOOKS.append(book)
    return book

# * PUT Method (Update a book)
@app.put('/books/{book_title}', response_model=Book, status_code=status.HTTP_200_OK)
async def update_book(book_title: str, updated_book: Book):
    for index, book in enumerate(BOOKS):
        if book.title.casefold() == book_title.casefold():
            BOOKS[index] = updated_book
            return updated_book
    
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")

# * DELETE Method (Delete a book)
@app.delete('/books/{book_title}', response_model=dict, status_code=status.HTTP_200_OK)
async def delete_book(book_title: str):
    for i, book in enumerate(BOOKS):
        if book.title.casefold() == book_title.casefold():
            BOOKS.pop(i)
            return {"message": "Book deleted successfully"}
    
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")

# * Endpoint to create book with BookRequest validation
class BookRequest(BaseModel):
    id: Optional[int] = Field(description="ID is not required to create a book", default=None)
    title: str = Field(min_length=2, max_length=80)
    author: str = Field(min_length=2, max_length=40)
    description: str = Field(min_length=2, max_length=200)
    category: str = Field(min_length=2, max_length=40)
    rating: int = Field(..., ge=1, le=5)
    
    model_config = {
        "json_schema_extra":{
            "example": {
                "title": "How to be...",
                "author": "Dev-Rajnish",
                "description": "This is a book about how to be a good person",
                "category": "Self-help",
                "rating": 5,
            }
        }
    }

@app.post("/bookObj/create_book/", response_model=Book, status_code=status.HTTP_201_CREATED)
async def create_book(Book_request: BookRequest):
    # Check if book already exists
    for book in BOOKS:
        if book.title.casefold() == Book_request.title.casefold():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Book already exists")
    
    new_book = Book(**Book_request.model_dump())
    new_book.id = generate_book_id(BOOKS)
    BOOKS.append(new_book)
    return new_book

# * Fetch book by ID (fix path conflict)
@app.get("/books/id/{book_id}", response_model=Book, status_code=status.HTTP_200_OK)
async def fetchBookByID(book_id: int = Path(gt=0)):
    for book in BOOKS:
        if book.id == book_id:
            return book
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")

# * Fetch book by rating
@app.get("/books/rating/{rating}", response_model=List[Book], status_code=status.HTTP_200_OK)
async def fetchBookByRating(rating: int = Path(..., ge=1, le=5)):
    books_to_return = [book for book in BOOKS if book.rating == rating]
    if not books_to_return:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No books found with this rating")
    return books_to_return

# * Update book by ID
@app.put("/books/update/{book_id}", response_model=Book, status_code=status.HTTP_200_OK)
async def updateBookByID(book_id: int, updated_book: Book):
    for index, book in enumerate(BOOKS):
        if book.id == book_id:
            BOOKS[index] = updated_book
            return updated_book
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")

# * Delete book by ID
@app.delete("/books/delete/{book_id}", response_model=dict, status_code=status.HTTP_200_OK)
async def deleteBookByID(book_id: int = Path(gt=0)):
    for i, book in enumerate(BOOKS):
        if book.id == book_id:
            BOOKS.pop(i)
            return {"message": "Book deleted successfully"}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models
from models import Todo
from pydantic import BaseModel

# * Create the database tables (Only needed if not using Alembic for migrations)
models.Base.metadata.create_all(bind=engine)

# * Initialize FastAPI app
app = FastAPI()

# * Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# * Pydantic model to validate incoming request data
class TodoRequest(BaseModel):
    title: str
    description: str
    priority: int
    complete_status: bool = False  # * Default value if not provided

# * API Endpoint: To Read all the TODO's in the database
@app.get("/")
async def readAllTodo(db: Session = Depends(get_db)):
    return db.query(Todo).all()


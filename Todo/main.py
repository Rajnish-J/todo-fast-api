from fastapi import FastAPI, Depends, HTTPException, status, Path
from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models
from models import Todo
from pydantic import BaseModel, Field

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
    title: str = Field(min_length=3)
    description: str = Field(min_length=3, max_length=100)
    priority: int = Field(gt=0, lt=6)
    complete_status: bool = False  # * Default value if not provided

# * API Endpoint: To Read all the TODO's in the database
@app.get("/read_All_TODO", status_code=status.HTTP_200_OK)
async def readAllTodo(db: Session = Depends(get_db)):
    if db.query(Todo).all() is not None:
        return db.query(Todo).all()
    raise HTTPException(status_code=404, detail="No data available")

# * API Endpoint: To read the todo using todo id
@app.get("/read_TODO/{id}", status_code=status.HTTP_200_OK)
async def readTODOByID(todo_id: int = Path(gt=0), db: Session = Depends(get_db)):
    ret_todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if ret_todo is not None:
        return ret_todo
    raise HTTPException(status_code=404, detail=f"TODO not found with id {todo_id}")


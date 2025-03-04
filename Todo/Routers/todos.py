from fastapi import APIRouter, Depends, HTTPException, status, Path
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Todo
from pydantic import BaseModel, Field

router = APIRouter(prefix="/todos", tags=["Todos"])

# * Pydantic model to validate incoming request data
class TodoRequest(BaseModel):
    title: str = Field(min_length=3)  # * Title must be at least 3 characters long
    description: str = Field(min_length=3, max_length=100)  # * Description must be 3-100 characters long
    priority: int = Field(gt=0, lt=6)  # * Priority should be between 1 and 5
    complete_status: bool = False  # ? Default value set to False if not provided

# * Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# * API Endpoint: To Read all the TODOs in the database
@router.get("/", status_code=status.HTTP_200_OK)
async def readAllTodo(db: Session = Depends(get_db)):
    todos = db.query(Todo).all()
    if todos:
        return todos
    raise HTTPException(status_code=404, detail="No data available")

# * API Endpoint: To read a TODO using its ID
@router.get("/{id}", status_code=status.HTTP_200_OK)
async def readTODOByID(todo_id: int = Path(gt=0), db: Session = Depends(get_db)):
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if todo:
        return todo
    raise HTTPException(status_code=404, detail=f"TODO not found with id {todo_id}")

# * API Endpoint: To add a TODO to the database
@router.post("/", status_code=status.HTTP_201_CREATED)
async def addTODO(todo: TodoRequest, db: Session = Depends(get_db)):
    todo_obj = Todo(**todo.model_dump())
    db.add(todo_obj)
    db.commit()
    return todo_obj

# * API Endpoint: To update an existing TODO in the database
@router.put("/{todo_id}", status_code=status.HTTP_200_OK)
async def updatetodo(todo: TodoRequest, db: Session = Depends(get_db), todo_id: int = Path(gt=0)):
    todo_obj = db.query(Todo).filter(Todo.id == todo_id).first()
    if not todo_obj:
        raise HTTPException(status_code=404, detail=f"TODO not found with id {todo_id}")
    
    todo_obj.title = todo.title
    todo_obj.description = todo.description
    todo_obj.priority = todo.priority
    todo_obj.complete_status = todo.complete_status
    
    db.commit()
    return todo_obj

# * API Endpoint: To delete a TODO by ID
@router.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def deleteTodo(db: Session = Depends(get_db), todo_id: int = Path(gt=0)):
    todo_obj = db.query(Todo).filter(Todo.id == todo_id).first()
    if not todo_obj:
        raise HTTPException(status_code=404, detail=f"TODO not found with id {todo_id}")
    
    db.query(Todo).filter(Todo.id == todo_id).delete()
    db.commit()
from fastapi import APIRouter, Depends, HTTPException, status, Path
from sqlalchemy.orm import Session
from models import Todo
from pydantic import BaseModel, Field
from database import get_db

router = APIRouter(prefix="/todos", tags=["Todos"])

class TodoRequest(BaseModel):
    title: str = Field(min_length=3)
    description: str = Field(min_length=3, max_length=100)
    priority: int = Field(gt=0, lt=6)
    complete_status: bool = False

@router.get("/", status_code=status.HTTP_200_OK)
async def read_all_todos(db: Session = Depends(get_db)):
    return db.query(Todo).all()

@router.get("/{id}", status_code=status.HTTP_200_OK)
async def read_todo_by_id(todo_id: int = Path(gt=0), db: Session = Depends(get_db)):
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if todo:
        return todo
    raise HTTPException(status_code=404, detail=f"TODO not found with id {todo_id}")

@router.post("/", status_code=status.HTTP_201_CREATED)
async def add_todo(todo: TodoRequest, db: Session = Depends(get_db)):
    todo_obj = Todo(**todo.model_dump())
    db.add(todo_obj)
    db.commit()
    return todo_obj

@router.put("/{todo_id}", status_code=status.HTTP_200_OK)
async def update_todo(todo: TodoRequest, db: Session = Depends(get_db), todo_id: int = Path(gt=0)):
    todo_obj = db.query(Todo).filter(Todo.id == todo_id).first()
    if not todo_obj:
        raise HTTPException(status_code=404, detail=f"TODO not found with id {todo_id}")
    
    todo_obj.title = todo.title
    todo_obj.description = todo.description
    todo_obj.priority = todo.priority
    todo_obj.complete_status = todo.complete_status
    
    db.commit()
    return todo_obj

@router.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(db: Session = Depends(get_db), todo_id: int = Path(gt=0)):
    todo_obj = db.query(Todo).filter(Todo.id == todo_id).first()
    if not todo_obj:
        raise HTTPException(status_code=404, detail=f"TODO not found with id {todo_id}")
    
    db.delete(todo_obj)
    db.commit()

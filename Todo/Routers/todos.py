from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status, Path
from sqlalchemy.orm import Session
from models import Todo
from pydantic import BaseModel, Field
from database import get_db
from Routers.auth import get_current_user

router = APIRouter(prefix="/todos", tags=["Todos"])
user_dependency = Annotated[dict, Depends(get_current_user)]

class TodoRequest(BaseModel):
    title: str = Field(min_length=3)
    description: str = Field(min_length=3, max_length=100)
    priority: int = Field(gt=0, lt=6)
    complete_status: bool = False

# * create todo with repective to user id
@router.post("/create_todo", status_code=status.HTTP_201_CREATED)
async def create_todo(user: user_dependency , todo: TodoRequest, db: Session = Depends(get_db)):
    if user is None:
        raise HTTPException(status_code=401, detail = "unauthorized")
    todo_obj = Todo(**todo.model_dump(), user_id = user.get('id'))
    db.add(todo_obj)
    db.commit()
    return todo_obj

# * get all todo by user id
@router.get("/getTodo_byUserID", status_code=status.HTTP_200_OK)
async def read_all_todos(user: user_dependency , db: Session = Depends(get_db)):
    if user is None:
        raise HTTPException(status_code=401, detail = "unauthorized")
    return db.query(Todo).filter(Todo.user_id == user.get('id')).all()

# * get todo by user and todo id
@router.get("/{todo_id}", status_code=status.HTTP_200_OK)
async def read_todo_by_id(user: user_dependency , todo_id: int = Path(gt=0), db: Session = Depends(get_db)):
    if user is None:
        raise HTTPException(status_code=401, detail = "unauthorized")
    todo = db.query(Todo).filter(Todo.todo_id == todo_id).filter(Todo.user_id == user.get('id')).first()
    if todo:
        return todo
    raise HTTPException(status_code=404, detail=f"TODO not found with id {todo_id}")

# * update todo by todo and user id
@router.put("/{todo_id}", status_code=status.HTTP_200_OK)
async def update_todo(user: user_dependency , todo: TodoRequest, db: Session = Depends(get_db), todo_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=401, detail = "unauthorized")
    todo_obj = db.query(Todo).filter(Todo.todo_id == todo_id).filter(Todo.user_id == user.get('id')).first().first()
    if not todo_obj:
        raise HTTPException(status_code=404, detail=f"TODO not found with id {todo_id}")
    
    todo_obj.title = todo.title
    todo_obj.description = todo.description
    todo_obj.priority = todo.priority
    todo_obj.complete_status = todo.complete_status
    
    db.commit()
    return todo_obj

# * delete todo by todo and user id
@router.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(user: user_dependency , db: Session = Depends(get_db), todo_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=401, detail = "unauthorized")
    todo_obj = db.query(Todo).filter(Todo.todo_id == todo_id).filter(Todo.user_id == user.get('id')).first().first()
    if not todo_obj:
        raise HTTPException(status_code=404, detail=f"TODO not found with id {todo_id}")
    
    db.delete(todo_obj)
    db.commit()

from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status, Path
from sqlalchemy.orm import Session
from models import Todo
from pydantic import BaseModel, Field
from database import get_db
from Routers.auth import get_current_user

router = APIRouter(prefix="/admin", tags=["admin"])
user_dependency = Annotated[dict, Depends(get_current_user)]

@router.get("/readAll_TodoByAdmin", status_code=status.HTTP_200_OK)
async def read_all_todo_by_admin(user: user_dependency, db: Session = Depends(get_db)):
    if user is None or user.get('role') != 'admin':
        raise HTTPException(status_code=401, detail="Authentication Failed")
    return db.query(Todo).all()

@router.delete("/deleteTodo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo_by_id_by_admin(user: user_dependency, todo_id : int = Path(gt=0), db: Session = Depends(get_db)):
    if user is None or user.get('role') != 'admin':
        raise HTTPException(status_code=401, detail="Authentication Failed")
    todo_delete =  db.query(Todo).filter(Todo.todo_id == todo_id).first()
    if todo_delete is None:
        raise HTTPException(status_code=404, detail = f"Todo not found with id {todo_id}")
    db.delete(todo_delete)
    db.commit()
    
    return {'detail': f"Todo Delete by admin with id {todo_id}"}
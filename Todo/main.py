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
        yield db  # * Yield the database session
    finally:
        db.close()  # ! Ensure database session is closed after use

# * Pydantic model to validate incoming request data
class TodoRequest(BaseModel):
    title: str = Field(min_length=3)  # * Title must be at least 3 characters long
    description: str = Field(min_length=3, max_length=100)  # * Description must be 3-100 characters long
    priority: int = Field(gt=0, lt=6)  # * Priority should be between 1 and 5
    complete_status: bool = False  # ? Default value set to False if not provided

# * API Endpoint: To Read all the TODOs in the database
@app.get("/read_All_TODO", status_code=status.HTTP_200_OK)
async def readAllTodo(db: Session = Depends(get_db)):
    if db.query(Todo).all() is not None:
        return db.query(Todo).all()  # * Return all TODOs from the database
    raise HTTPException(status_code=404, detail="No data available")  # ! Raise error if no data found

# * API Endpoint: To read a TODO using its ID
@app.get("/read_TODO/{id}", status_code=status.HTTP_200_OK)
async def readTODOByID(todo_id: int = Path(gt=0), db: Session = Depends(get_db)):
    ret_todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if ret_todo is not None:
        return ret_todo  # * Return the found TODO
    raise HTTPException(status_code=404, detail=f"TODO not found with id {todo_id}")  # ! Raise error if not found

# * API Endpoint: To add a TODO to the database
@app.post("/addtodo", status_code=status.HTTP_201_CREATED)
async def addTODO(todo: TodoRequest, db: Session = Depends(get_db)):
    todo_obj = Todo(**todo.model_dump())  # * Convert Pydantic model to SQLAlchemy model
    db.add(todo_obj)  # * Add new TODO to the session
    db.commit()  # * Commit changes to the database
    return todo_obj  # * Return the created TODO object

# * API Endpoint: To update an existing TODO in the database
@app.put("/Updatetodo/{todo_id}", status_code=status.HTTP_200_OK)
async def updatetodo(todo: TodoRequest, db: Session = Depends(get_db), todo_id: int = Path(gt=0)):
    todo_obj = db.query(Todo).filter(Todo.id == todo_id).first()
    if todo_obj is None:
        raise HTTPException(status_code=404, detail=f"TODO not found with id {todo_id}")  # ! Raise error if not found
    
    # TODO Updating the TODO object with new values
    todo_obj.title = todo.title
    todo_obj.description = todo.description
    todo_obj.priority = todo.priority
    todo_obj.complete_status = todo.complete_status
    
    db.add(todo_obj)  # ? No need to add explicitly; modifying the object is enough
    db.commit()  # * Commit the changes to the database
    
    return todo_obj  # * Return updated TODO object

# * API Endpoint: To delete a TODO by ID
@app.delete("/deletetodo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def deleteTodo(db: Session = Depends(get_db), todo_id: int = Path(gt=0)):
    todo_obj = db.query(Todo).filter(Todo.id == todo_id).first()
    if todo_obj is None:
        raise HTTPException(status_code=404, detail=f"TODO not found with id {todo_id}")  # ! Raise error if not found
    
    db.query(Todo).filter(Todo.id == todo_id).delete()  # TODO Delete the TODO from the database
    db.commit()  # * Commit the delete action to the database

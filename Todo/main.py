from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models
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

# * API Endpoint: Create a new To-Do item
@app.post("/todos/", status_code=status.HTTP_201_CREATED)
def create_todo(todo: TodoRequest, db: Session = Depends(get_db)):
    """
    * Create a new To-Do item and store it in the database.

    * Args:
        * - todo (TodoRequest): The incoming todo object from the request.
        * - db (Session): The database session dependency.

    * Returns:
        * - dict: The stored todo item with an auto-generated ID.
    """
    try:
        # * Basic Validation
        if not todo.title.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Title cannot be empty."
            )
        if todo.priority < 1 or todo.priority > 5:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Priority must be between 1 and 5."
            )

        new_todo = models.Todo(
            title=todo.title,
            description=todo.description,
            priority=todo.priority,
            complete_status=todo.complete_status
        )
        db.add(new_todo)  # * Add the object to the session
        db.commit()  # * Commit the transaction
        db.refresh(new_todo)  # * Refresh to get the updated object with ID

        return {"message": "Todo created successfully!", "todo": new_todo}

    except Exception as e:
        db.rollback()  # * Rollback in case of error
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred: {str(e)}"
        )

from fastapi import FastAPI, Depends
from database import engine, SessionLocal
import models
from Routers import todos, auth, users
from sqlalchemy.orm import Session
from database import get_db

# * Create the database tables (Only needed if not using Alembic for migrations)
models.Base.metadata.create_all(bind=engine)

# * Initialize FastAPI app
app = FastAPI()

# * Include routers
app.include_router(todos.router, dependencies=[Depends(get_db)])
app.include_router(auth.router, dependencies=[Depends(get_db)])
app.include_router(users.router, dependencies=[Depends(get_db)])

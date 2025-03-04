from fastapi import FastAPI
from database import engine, SessionLocal
import models
from Routers import todos, auth

# * Create the database tables (Only needed if not using Alembic for migrations)
models.Base.metadata.create_all(bind=engine)

# * Initialize FastAPI app
app = FastAPI()

# * Include routers for todos and auth
app.include_router(todos.router)
app.include_router(auth.router)

# * Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db  # * Yield the database session
    finally:
        db.close()  # ! Ensure database session is closed after use
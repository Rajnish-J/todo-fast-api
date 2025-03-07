from fastapi import APIRouter, Depends, HTTPException, status, Path
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from database import SessionLocal
from models import Users
from passlib.context import CryptContext
from database import get_db

router = APIRouter(prefix="/user", tags=["User"])
bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated="auto")

# * Request Model for Creating Users
class UserRequest(BaseModel):
    email: str = Field(max_length=50)
    username: str = Field(max_length=30)
    firstname: str = Field(max_length=15)
    lastname: str = Field(max_length=15)
    password: str = Field(min_length=8, max_length=72)
    is_active: bool
    role: str = Field(max_length=15)

# * Create New User
@router.post("/createUser", status_code=status.HTTP_201_CREATED)
async def create_user(create_user: UserRequest, db: Session = Depends(get_db)):
    hashed_password = bcrypt_context.hash(create_user.password)
    user_obj = Users(
        email=create_user.email,
        username=create_user.username,
        firstname=create_user.firstname,
        lastname=create_user.lastname,
        password=hashed_password,
        is_active=create_user.is_active,
        role=create_user.role
    )

    db.add(user_obj)
    db.commit()
    db.refresh(user_obj)
    return {"message": "User created successfully"}

# * Fetch User by ID
@router.get("/fetchuserbyid/{id}", status_code=status.HTTP_200_OK)
async def fetch_user_by_id(id: int = Path(gt=0), db: Session = Depends(get_db)):
    user = db.query(Users).filter(Users.id == id).first()
    if user:
        return user
    raise HTTPException(status_code=404, detail="No user found")

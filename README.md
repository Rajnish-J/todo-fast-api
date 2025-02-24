# FastAPI Course - Complete Notes

This document serves as a structured **study guide** and **reference** for FastAPI, including key concepts, setup steps, authentication, database integration, deployment, and useful commands.

---

## 📌 Table of Contents
1. [Introduction to FastAPI](#introduction-to-fastapi)
2. [Setting Up the Environment](#setting-up-the-environment)
3. [FastAPI Core Concepts](#fastapi-core-concepts)
4. [Database Integration with SQLAlchemy](#database-integration-with-sqlalchemy)
5. [Authentication & JWT Security](#authentication--jwt-security)
6. [Middleware & Dependency Injection](#middleware--dependency-injection)
7. [Testing in FastAPI](#testing-in-fastapi)
8. [Deployment Strategies](#deployment-strategies)
9. [Advanced Topics](#advanced-topics)
10. [Useful Commands & Snippets](#useful-commands--snippets)

---

## 🚀 Introduction to FastAPI
FastAPI is a **modern, high-performance** web framework for building APIs with Python 3.6+.

### 🔥 Key Features:
- **Blazing Fast** 🚀 (Asynchronous support using `async` & `await`).
- **Built-in Data Validation** using **Pydantic**.
- **Auto-generated API Docs** with **Swagger UI** & **ReDoc**.
- **Dependency Injection** for modular development.
- **Asynchronous Database Support** (SQLAlchemy, TortoiseORM).
- **Production-Ready** (uses Uvicorn ASGI server).

---

## 🛠️ Setting Up the Environment

### 📌 Install Python 3.6+ (Check version)
```bash
python3 --version
```

### 📌 Create a Virtual Environment
```bash
python3 -m venv fastapi_env
```

### 📌 Activate Virtual Environment
- **macOS/Linux**:
  ```bash
  source fastapi_env/bin/activate
  ```
- **Windows**:
  ```bash
  fastapi_env\Scripts\activate
  ```

### 📌 Install Required Dependencies
```bash
pip install fastapi uvicorn sqlalchemy alembic psycopg2-binary passlib bcrypt python-jose python-multipart
```

### 📌 Run FastAPI Server
```bash
uvicorn main:app --reload
```

### 📌 Check Auto-generated Docs:
- **Swagger UI**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **ReDoc UI**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## 📖 FastAPI Core Concepts

### 1️⃣ **Creating a Simple FastAPI App**
```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}
```

### 2️⃣ **Dynamic Routing with Path Parameters**
```python
@app.get("/users/{user_id}")
def get_user(user_id: int):
    return {"user_id": user_id}
```

### 3️⃣ **Query Parameters**
```python
@app.get("/items/")
def read_items(skip: int = 0, limit: int = 10):
    return {"skip": skip, "limit": limit}
```

### 4️⃣ **Request Body with Pydantic**
```python
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    price: float
    description: str = None

@app.post("/items/")
def create_item(item: Item):
    return {"item_name": item.name, "item_price": item.price}
```

---

## 🗄️ Database Integration with SQLAlchemy

### 1️⃣ **Configure SQLAlchemy**
```python
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
```

### 2️⃣ **Define a Database Model**
```python
from sqlalchemy import Column, Integer, String

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
```

### 3️⃣ **Create Database Tables**
```bash
python -c 'from database import Base, engine; Base.metadata.create_all(bind=engine)'
```

---

## 🔐 Authentication & JWT Security

### 1️⃣ **Install Authentication Dependencies**
```bash
pip install passlib bcrypt python-jose python-multipart
```

### 2️⃣ **Password Hashing**
```python
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)
```

### 3️⃣ **JWT Token Authentication**
```python
from jose import JWTError, jwt
from datetime import datetime, timedelta

SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
```

---

## ⚡ Middleware & Dependency Injection
### 1️⃣ **CORS Middleware**
```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### 2️⃣ **Dependency Injection**
```python
from fastapi import Depends

def common_parameters(q: str = None):
    return {"q": q}

@app.get("/items/")
def read_items(commons: dict = Depends(common_parameters)):
    return commons
```

---

## 🧪 Testing in FastAPI

### 1️⃣ **Install Pytest**
```bash
pip install pytest httpx
```

### 2️⃣ **Write a Test**
```python
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello, FastAPI!"}
```

### 3️⃣ **Run Tests**
```bash
pytest
```

---

## 🌎 Deployment Strategies

### 1️⃣ **Run with Uvicorn in Production**
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

### 2️⃣ **Deploy to Docker**
- Create a `Dockerfile`:
```dockerfile
FROM python:3.9
WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```
- Build & Run:
```bash
docker build -t fastapi-app .
docker run -d -p 8000:8000 fastapi-app
```

---

## 📚 Advanced Topics
- WebSockets with FastAPI
- Background Tasks
- GraphQL with FastAPI
- Async Database (TortoiseORM)
- Microservices with FastAPI

---

## 🔧 Useful Commands & Snippets

### 🌍 General Commands
```bash
pip freeze > requirements.txt
uvicorn main:app --reload
```

### 🔧 Database Commands
```bash
sqlite3 test.db
```

### 🏗️ Alembic Migration
```bash
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head
```

---
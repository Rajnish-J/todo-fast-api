from fastapi import FastAPI

app = FastAPI()

@app.get("/about")
def greet():
    return {"message": "Hello, World!"}
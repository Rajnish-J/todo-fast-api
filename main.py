from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel

class Blog(BaseModel):
    title: str
    body: str
    published: Optional[bool]
    referableLinks: Optional[str]

app = FastAPI()

@app.get("/home")
def home():
    return "Hello from home page"

@app.get("/about")
def blog():
    return "about page from the blog"

@app.get("/blog")
def blog(limit=10, published:bool = True, sort: Optional[str] = None):
    if(published):
        return {'data': f'{limit} blogs from the published'}
    return {'data': f'{limit} blogs from the unpublished'}

@app.get('/blog/unpublished')
def unpublished():
    return {'data': 'all unpublished blogs'}

@app.get("/blog/{id}")
def blog(id:int):
    return {'data': id}


@app.get("/blog/{id}/comments")
def blogComments(id:int):
    return {'data': {'good video', 'Fantastic teaching'}}

# ! post methods

@app.post("/blog")
def create_blog():
    return {'data': 'Blog is created successfully'}
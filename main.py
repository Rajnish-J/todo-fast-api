# * Import statements

from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel

# * General Class
class Blog(BaseModel):
    title: str
    body: str
    published: Optional[bool]
    referableLinks: Optional[str]

app = FastAPI()

# * GET mothods

# ? normal get request with the path as / and it returns the string
@app.get("/home")
def home():
    return "Hello from home page"

# ? normal get request with the path as / and it returns the string
@app.get("/about")
def blog():
    return "about page from the blog"

# ? normal get method that accepts the parameters and limits and return the data with conditional statements
@app.get("/blog")
def blog(limit=10, published:bool = True, sort: Optional[str] = None):
    if(published):
        return {'data': f'{limit} blogs from the published'}
    return {'data': f'{limit} blogs from the unpublished'}

# ? show the path
@app.get('/blog/unpublished')
def unpublished():
    return {'data': 'all unpublished blogs'}

# ? show the path with the id (so far query parameters are used)
@app.get("/blog/{id}")
def blog(id:int):
    return {'data': id}

# ? show the path with the id and the comments
@app.get("/blog/{id}/comments")
def blogComments(id:int):
    return {'data': {'good video', 'Fantastic teaching'}}

# ! post methods

# ? In the request we can use any name instead of the request but the name could be used in the same way in the function
@app.post("/createBlog")
def create_blog(request: Blog):
    return {'data': f'Blog is created with title as {request.title} and body as {request.body} and published as {request.published} and referableLinks as {request.referableLinks}'}


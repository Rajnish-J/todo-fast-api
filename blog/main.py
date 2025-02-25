# the separate blog for connection to the db

# * Import statements

from fastapi import FastAPI

# * scheama import

from . import schemas

app = FastAPI()

@app.post("/createBlog")
def createBlog(request: schemas.Blog):
    return {'data': f'Blog is created with title as {request.title} and body as {request.body}'}
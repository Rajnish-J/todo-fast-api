from fastapi import FastAPI

app = FastAPI()

@app.get("/home")
def home():
    return "Hello from home page"

@app.get("/about")
def blog():
    return "about page from the blog"

@app.get('/blog/unpublished')
def unpublished():
    return {'data': 'all unpublished blogs'}

@app.get("/blog/{id}")
def blog(id:int):
    return {'data': id}


@app.get("/blog/{id}/comments")
def blogComments(id:int):
    return {'data': {'good video', 'Fantastic teaching'}}
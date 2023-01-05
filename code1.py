# Create a virtual environment
# Change python interpreter to virtual environment (<venv-name>\scripts\python.exe)
# Activate virtual environment 
# Install dependencies
    # pip install fastapi[all]
# Start up web server
    # uvicorn main:app --reload


from fastapi import FastAPI
from pydantic import BaseModel
from random import randrange


app = FastAPI()

class Template(BaseModel):
    title: str
    content: str
    publish: int = True

my_posts = [{"title": "favourite foods", "content": "pizaz", "id": 1}, {"title": "losmnd", "content": "ff", "id": 2}]


@app.get("/")
def root():
    return {"data": "Welcome to the homepage."}

@app.get("/posts")
def get_posts():
    return {"data": my_posts}

@app.post("/posts/create")
def create_post(post: Template):
    postdict = post.dict()
    postdict["id"] = randrange(0, 100000)
    my_posts.append(postdict)
    if post.publish is True:
        return {f"Your post titled '{post.title}' has been published."}
    else:
        return {"Draft saved."}

@app.get("/posts/{id}")
def get_individual_post(id: int):
    for x in my_posts:
        if x["id"] == id:
            return {"data": x}
    return {f"Post with id of {id} was not found"}

@app.put("/posts/{id}")
def update_post(id:int, post: Template):
    for x in my_posts:
        if x["id"] == id:
            my_posts.pop(my_posts.index(x))
            post = dict(post)
            post["id"] = id
            my_posts.append(post)
            return {"data": "Post updated"}
    return {"data": f"Post with id of {id} was not found"}
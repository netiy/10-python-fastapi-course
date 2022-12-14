from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel
from random import randrange

app = FastAPI()

class Template(BaseModel):
    title: str
    content: str
    publish: int = True
    rating: Optional[int] = None

my_posts = [{"title": "favourite foods", "content": "pizaz", "id": 1}, {"title": "losmnd", "content": "ff", "id": 1}]
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

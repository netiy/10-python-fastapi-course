# Create and activate virtual environment for project
    # py -3 -m venv fastapi-venv
    # fastapi-venv\scripts\activate.bat
# Install dependencies 
    # pip install fastapi[all]
    # pip install psycopg2
# Change python interpreter to \fastapi-venv\scripts\python.exe
# Create a table in postgres, and rename the values in line 30
# Start up web server
    # uvicorn main:app --reload


    
from fastapi import FastAPI, status, HTTPException
from psycopg2.extras import RealDictCursor
from pydantic import BaseModel
from time import sleep
import psycopg2



class UserCreatePost(BaseModel):
    title: str
    content: str
    published: bool = True

app = FastAPI()
while True:
    try:
        conn = psycopg2.connect(host="localhost", database="fastapi", user="postgres", password="password123", cursor_factory=RealDictCursor)
        print("Database connection was successful")
        cursor = conn.cursor()
        break
    except Exception as error:
        print("Database connnection has failed")
        print("Error: ", error)
        sleep(3)


@app.get("/")
def root():
    return {"root"}


@app.get("/posts")
def get_posts():
    cursor.execute("""SELECT * FROM posts""")
    posts = cursor.fetchall()
    return {"data": posts}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: UserCreatePost):
    cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""", (post.title, post.content, post.published,))
    post = cursor.fetchone()
    conn.commit()
    return {"data": post}

@app.put("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def update_post(id: int, post: UserCreatePost):
    cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""", (post.title, post.content, post.published, str(id),))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    conn.commit()
    return {"data": f"Post with id of {id} has been updated"}

@app.get("/posts/{id}")
def get_individual_post(id: int):
    cursor.execute("""SELECT * FROM posts WHERE id = %s""", (str(id),))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return {"data": post}

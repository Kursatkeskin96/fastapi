from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
import psycopg as psycopg3
from psycopg.rows import dict_row  # Import dict_row correctly for cursor context
import time
from sqlalchemy.orm import Session
from . import models
from .database import  engine, get_db


# Create the tables if they don't exist
models.Base.metadata.create_all(bind=engine)

app = FastAPI()




class Post(BaseModel):
    title: str
    content: str
    published: bool = True

while True:
    try:
        # Establish connection to PostgreSQL database
        conn = psycopg3.connect(
            host='localhost',
            dbname='fastapi',
            user='postgres',
            password='test123'
        )
        print("DB connected")
        break  # Exit the loop if the connection is successful
    except Exception as error:
        print(f"Error connecting to the database: {error}")
        time.sleep(2)  # Retry every 2 seconds

class PostUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    published: Optional[bool] = None

my_posts = [{"title": "title of test", "id": 1}]


def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p

def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i

@app.get("/")
async def root():
    return {"message": "Hello world"}


@app.get("/posts")
async def get_posts():
    # Use cursor with dict_row to get rows as dictionaries
    with conn.cursor(row_factory=dict_row) as cursor:
        cursor.execute("SELECT * FROM posts")
        posts = cursor.fetchall()
        print(posts)
    return {"data": posts}


@app.get("/posts/{id}")
async def get_post(id: int, response: Response):
    with conn.cursor(row_factory=dict_row) as cursor:
        # Properly execute the SQL query with the id as a tuple
        cursor.execute("SELECT * from posts WHERE id = %s", (id,))
        # Fetch one result from the database
        post = cursor.fetchone()
        print(post)
        
        if not post:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
    
    return {"post_detail": post}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    # Use cursor with dict_row to get rows as dictionaries
    with conn.cursor(row_factory=dict_row) as cursor:
        # Use RETURNING to get the inserted row
        cursor.execute(
            "INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *",
            (post.title, post.content, post.published)
        )
        # Fetch the newly inserted post
        new_post = cursor.fetchone()
        # Commit the transaction
        conn.commit()

    return {"data": new_post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_posts(id: int):
   with conn.cursor(row_factory=dict_row) as cursor:
    
    cursor.execute("DELETE FROM posts WHERE id = %s returning *",(str(id),))   
    deleted_post = cursor.fetchone()
    conn.commit()


    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with {id} does not exist")

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_post(id: int, post: Post):

    with conn.cursor() as cursor:
        cursor.execute(
            "UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s",
            (post.title, post.content, post.published, id)
        )
        update_post = cursor.fetchone()

    if update_post == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Post with id {id} does not exist"
        )
    return {"data": update_post}


@app.patch("/posts/{id}")
def patch_post(id: int, post: PostUpdate):
    # Prepare a list of fields to update dynamically
    update_fields = []
    update_values = []
    
    # Check if the fields are provided in the request body
    if post.title is not None:
        update_fields.append("title = %s")
        update_values.append(post.title)
    if post.content is not None:
        update_fields.append("content = %s")
        update_values.append(post.content)
    if post.published is not None:
        update_fields.append("published = %s")
        update_values.append(post.published)

    # If there is nothing to update, raise an exception
    if not update_fields:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No fields provided to update")

    # Add the id to the list of values to bind in the query
    update_values.append(id)

    update_query = f"UPDATE posts SET {', '.join(update_fields)} WHERE id = %s RETURNING *"

    with conn.cursor(row_factory=dict_row) as cursor:
        # Execute the dynamic update query
        cursor.execute(update_query, tuple(update_values))
        updated_post = cursor.fetchone()
        conn.commit()

    # If the post does not exist, raise a 404 error
    if updated_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} does not exist")

    return {"data": updated_post}

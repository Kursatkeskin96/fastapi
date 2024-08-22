from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


class PostUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    published: Optional[bool] = None
    rating: Optional[int] = None


my_posts = [{"title": "title of test", "id": 1}]


def find_post(id):
    for p in my_posts:
        if p ["id"] == id:
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
    return {"data": my_posts}



@app.get("/posts/{id}")
async def get_post(id: int, response: Response):
    post = find_post(id)
    if not post:
       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
    return {"post_detail": post}




@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    print(post)
    post_dict = post.model_dump()
    post_dict['id'] = randrange(0, 1000000)
    my_posts.append(post_dict)
    return {"data": post_dict}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_posts(id: int):

    index = find_index_post(id)

    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with {id} does not exist")

    my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
    


@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    # Find the index of the post to update
    index = find_index_post(id)
    if index is None:  # If post not found
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Post with id {id} does not exist"
        )
    # Convert Pydantic model to a dictionary using model_dump()
    post_dict = post.model_dump()
    post_dict['id'] = id  # Ensure the post keeps the same id
    
    # Update the post in the list
    my_posts[index] = post_dict

    return {"data": post_dict}


@app.patch("/posts/{id}")
def patch_post(id: int, post: PostUpdate):
    index = find_index_post(id)
    if index is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Post with id {id} does not exist"
        )
    
    existing_post = my_posts[index]
    
    # Update only the fields that are provided in the request
    updated_post = existing_post.copy()
    
    if post.title is not None:
        updated_post["title"] = post.title
    if post.content is not None:
        updated_post["content"] = post.content
    if post.published is not None:
        updated_post["published"] = post.published
    
    updated_post['id'] = id  # Ensure the post ID stays the same
    
    my_posts[index] = updated_post

    return {"data": updated_post}
       
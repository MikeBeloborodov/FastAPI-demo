from typing import Optional
from fastapi import FastAPI, Response, status, Body, HTTPException
from pydantic import BaseModel
import database
import os

app = FastAPI()

"""
You can use Body from fastAPI body to get data, but you can also
use pydantic
@app.post("/postdata")
def get_post(body: dict = Body(...)):
    return {"Your message" : body}  
"""
# this is pydantic model
class Post(BaseModel):
    title: str
    content: str
    rating: Optional[int] = 0

@app.post("/posts")  
def post_new_post(new_post: Post):
    if os.path.exists("posts.db"):
        database.save_post(new_post)
    else:
        database.create_db()
        database.save_post(new_post)
    # convert pydantic into dictionary
    # data = new_post.dict()
    return {"Your message" : new_post}

@app.get("/posts")
def send_all_posts():
    if os.path.exists("posts.db"):
        posts_list = database.get_all_posts()
        if not posts_list:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Database is empty")
            #response.status_code = status.HTTP_404_NOT_FOUND
            #return {"Message" : "Database is empty"}
        posts_dict = database.convert_to_json(posts_list)
        return {"All posts" : posts_dict}
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="There is no database yet")

@app.get("/posts/{id}")
def send_post_by_id(id: int):
    if os.path.exists("posts.db"):
        post_list = database.get_post_by_id(id)
        post_dict = database.convert_to_json(post_list)
        if post_dict:
            return {f"Post #{id}" : post_dict}
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="There is no such post")
    else: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="There is no database yet")
    
@app.put("/posts/{id}")
def update_post_by_id(id: int, updated_post: Post):
    if os.path.exists("posts.db"):
        if database.update_post_by_id(id, updated_post):
            return {"Message" : "Your post has been updated successfully"}
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="There is no such post")
    else: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="There is no database yet")

@app.delete("/posts/{id}")
def delete_post_by_id(id: int):
    if os.path.exists("posts.db"):
        if database.delete_post_by_id(id):
            return {"Message" : "Your post has been deleted successfully"}
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="There is no such post")
    else: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="There is no database yet")

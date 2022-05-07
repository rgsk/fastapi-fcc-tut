from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from pydantic import BaseModel


app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


@app.get('/')
def root():
    return {"message": "Hello World"}


posts = []


@app.get('/posts')
def get_posts():
    return posts


@app.get('/posts/latest')
def get_latest_post():
    if len(posts) > 0:
        return posts[-1]


@app.get('/posts/{id}')
def get_post(id: int, response: Response):
    for post in posts:
        if post['id'] == id:
            return post
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f'no post found with id {id}')
    # response.status_code = status.HTTP_404_NOT_FOUND
    # return {
    #     'message': f'no post found with id {id}'
    # }


@app.post('/posts', status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    created_post = post.dict()
    created_post['id'] = len(posts)
    posts.append(created_post)
    # respose.status_code = status.HTTP_201_CREATED
    return created_post


@app.patch('/posts/{id}')
def update_post():
    return {}


@app.delete('/posts/{id}')
def delete_post(id):
    return {}

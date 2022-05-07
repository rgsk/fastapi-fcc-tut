from optparse import Option
from typing import List, Optional
from fastapi import FastAPI, Response, status, HTTPException
from pydantic import BaseModel


app = FastAPI()


class Post(BaseModel):
    id: int
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


class CreatePostInput (Post):
    id: None = None


class UpdatePostInput(BaseModel):
    title: Optional[str]
    content: Optional[str]
    published: Optional[bool]
    rating: Optional[int]


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

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f'posts are empty')


@app.get('/posts/{id}')
def get_post(id: int):
    for post in posts:
        if post['id'] == id:
            return post
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f'no post found with id {id}')


@app.post('/posts', status_code=status.HTTP_201_CREATED)
def create_post(post: CreatePostInput):
    created_post = post.dict()
    created_post['id'] = len(posts)
    posts.append(created_post)
    return created_post


@app.patch('/posts/{id}')
def update_post(id: int, data: UpdatePostInput):
    for p in posts:
        if p['id'] == id:
            if data.title != None:
                p['title'] = data.title
            if data.content != None:
                p['content'] = data.content
            if data.published != None:
                p['published'] = data.published
            if data.rating != None:
                p['rating'] = data.rating
            return p
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f'no post found with id {id}')


@app.delete('/posts/{id}')
def delete_post(id: int):
    for i, p in enumerate(posts):
        if p['id'] == id:
            posts.pop(i)
            return Response(status_code=status.HTTP_204_NO_CONTENT)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f'no post found with id {id}')

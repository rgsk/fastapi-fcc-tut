from typing import Optional
from fastapi import Body, FastAPI
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


@app.post('/posts')
def create_post(post: Post):
    created_post = post.dict()
    created_post['id'] = len(posts)
    posts.append(created_post)
    return created_post


@app.delete('/posts')
def delete_post():
    return {}

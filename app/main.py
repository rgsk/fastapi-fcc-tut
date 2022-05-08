from turtle import home, pos, pu
from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor

# we are 4:31 in video

app = FastAPI()

try:
    conn = psycopg2.connect(
        host="localhost",
        database="fastapi_fcc",
        user="postgres",
        password="postgres",
        cursor_factory=RealDictCursor
    )
    cursor = conn.cursor()
    print('Database connection successfull')
except Exception as error:
    print('Connecting to database failed')
    print('Error: ', error)


class Post(BaseModel):
    id: int
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None
    created_at: str


class CreatePostInput (Post):
    id: None = None
    created_at: None = None


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
    cursor.execute("""
        SELECT * FROM posts
    """)
    posts = cursor.fetchall()
    return posts


@app.get('/posts/latest')
def get_latest_post():
    if len(posts) > 0:
        return posts[-1]

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f'posts are empty')


def get_post_by_id(id: int):
    cursor.execute("""
        SELECT * from posts 
        WHERE id = %s
    """, (id,))
    post = cursor.fetchone()
    return post


@app.get('/posts/{id}')
def get_post(id: int):
    post = get_post_by_id(id)
    if post != None:
        return post
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'no post found with id {id}')


@app.post('/posts', status_code=status.HTTP_201_CREATED)
def create_post(post: CreatePostInput):
    cursor.execute("""
        INSERT INTO posts 
        (title, content, published, rating)
        VALUES
        (%s, %s, %s, %s)
        RETURNING *
    """, (
        post.title,
        post.content,
        post.published,
        post.rating
    ))
    conn.commit()
    new_post = cursor.fetchone()
    return new_post


@app.patch('/posts/{id}')
def update_post(id: int, data: UpdatePostInput):
    post_to_update = get_post_by_id(id)
    if post_to_update == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'no post found with id {id}')

    if data.title != None:
        post_to_update['title'] = data.title
    if data.content != None:
        post_to_update['content'] = data.content
    if data.published != None:
        post_to_update['published'] = data.published
    if data.rating != None:
        post_to_update['rating'] = data.rating

    cursor.execute("""
        UPDATE posts
        SET 
        title=%s, content=%s, published=%s, rating=%s
        WHERE
        id=%s
        RETURNING *
    """, (post_to_update['title'], post_to_update['content'], post_to_update['published'],
          post_to_update['rating'], id
          ))
    conn.commit()
    updated_post = cursor.fetchone()
    return updated_post


@app.delete('/posts/{id}')
def delete_post(id: int):
    cursor.execute("""
        DELETE FROM posts
        WHERE id = %s 
        RETURNING *
    """, (id,))
    conn.commit()
    post = cursor.fetchone()
    if post != None:
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f'no post found with id {id}')

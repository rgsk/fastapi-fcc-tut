from fastapi import FastAPI

app = FastAPI()


@app.get('/')
def root():
    return {"message": "Hello World changed 12312312"}


@app.get('/login')
def login():
    return {"message": "Within a year"}


posts = [{"id": 1, "text": "first post"}]


@app.get('/posts')
def get_posts():
    return posts

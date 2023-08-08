from fastapi import FastAPI

from router import blog_get
from router import blog_post
from router import user
from router import article

from db import models
from db.database import engine

# uvicorn main:app --reload
# Create database
# fastapi 인스턴스 생성
app = FastAPI()
app.include_router(blog_get.router)
app.include_router(blog_post.router)
app.include_router(user.router)
app.include_router(article.router)
@app.get("/hello")

def index2():
    return "Hi"

# DB 변경을 원하면 생성된 db 파일 삭제
models.Base.metadata.create_all(engine)
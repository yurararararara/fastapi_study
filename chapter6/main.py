from fastapi import FastAPI, status, Response
from enum import Enum
from typing import Optional
from router import blog_get
from router import blog_post
# fastapi-venv\Scripts\activate
# uvicorn main:app --reload

# fastapi 인스턴스 생성
app = FastAPI()
app.include_router(blog_get.router)
app.include_router(blog_post.router)
@app.get("/hello")
def index2():
    return "Hi"

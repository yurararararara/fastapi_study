from fastapi import FastAPI
from enum import Enum
from typing import Optional
# fastapi-venv\Scripts\activate
# uvicorn main:app --reload

# fastapi 인스턴스 생성
app = FastAPI()
# get = 데이터 읽기
# post = 데이터 생성
# put = 데이터 업데이트
# delete = 데이터 삭제
@app.get('/')
def index():
    return {"message" : "Hello World!"}
# {"detail":"Method Not Allowed"}
@app.post("/hello")
def index2():
    return "Hi"

# all과 type이 id보다 먼저 정의되어야 한다. 
# Query parameters and Path parameters
# Query - api 뒤에 데이터 입력, path - 서버에 직접 값 전달.
# http://127.0.0.1:8000/blog/45/comments/2?valid=false&username=alex
# : page and page_size
# 1
@app.get("/blog/all")
# Default values
# def get_all_blogs(page = 1, page_size = 10):
# Optional parameters
def get_all_blogs(page = 1, page_size : Optional[int] = None):
    # return {"message" : "All blogs provided"}
    return {"message" : f"All {page_size} blogs on page {page}"}

# 2
# Predefined path
# Predefined values with Enum
class BlogType(str, Enum):
    short = 'short'
    story = 'story'
    howto = 'howto'

@app.get("/blog/type/{type}")
def blog_type(type : BlogType):
    return {"message" : f"Blog type : {type}"}
# 3
# Query parameter & Path parameters
@app.get('/blog/{id}/comments/{comment_id}')
def get_comment(id : int, comment_id : int, valid : bool = True, username : Optional[str] = None):
    return {"message" : f"blog_id {id}, comment_id {comment_id}, valid {valid}, username {username}"}
# 4
# status code 지정 방법 두가지
@app.get('/blog/{id}')
# Type validation 타입을 지정하면 다른 타입이 들어오면 error 메세지
def get_blog(id : int):
        return {"message" : f"Blog with id {id}"}
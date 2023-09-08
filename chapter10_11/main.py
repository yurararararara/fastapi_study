from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse, PlainTextResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from router import blog_get, blog_post, user, article, product, file 
from auth import authentication

from db import models
from db.database import engine
from exceptions import StoryException
# uvicorn main:app --reload
# Create database
# fastapi 인스턴스 생성
app = FastAPI()
app.include_router(authentication.router)
app.include_router(file.router)
app.include_router(blog_get.router)
app.include_router(blog_post.router)
app.include_router(user.router)
app.include_router(article.router)
app.include_router(product.router)
@app.get("/hello")

def index2():
    return "Hi"

# 사용자 정의 예외 클래스
@app.exception_handler(StoryException)
def story_exception_handler(request: Request, exc: StoryException):
    return JSONResponse(
        status_code=418,
        content= {'detail': exc.name}
    )
# 기본적인 HTTP 예외를 처리하기 위한 함수
@app.exception_handler(HTTPException)
def custom_handler(request: Request, exc: StoryException):
    return PlainTextResponse(str(exc), status_code=400)

# DB 변경을 원하면 생성된 db 파일 삭제
models.Base.metadata.create_all(engine)
# CORS 미들웨어 추가
# 다른 도메인에서 온 요청을 처리하기 위해 필요한 보안 관련 설정 제공
origins = [
    'http://localhost:3000'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"]
)
# file
# upload file
# making files statically available
# Downloading files


# localhost:8000/files/fubao1.jpg
# Fastapi 내부에서 정적 파일(HTML, CSS, 이미지 파일 등)서비스하거나 관리할 수 있다. 
app.mount("/files", StaticFiles(directory="files"), name="files")


# Deta
# 무료 클라우드 서비스
# https://deta.space/
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse, PlainTextResponse
from fastapi.middleware.cors import CORSMiddleware
from router import blog_get
from router import blog_post
from router import user
from router import article
from router import product
from auth import authentication

from db import models
from db.database import engine
from exceptions import StoryException
# uvicorn main:app --reload
# Create database
# fastapi 인스턴스 생성
app = FastAPI()
app.include_router(blog_get.router)
app.include_router(blog_post.router)
app.include_router(user.router)
app.include_router(article.router)
app.include_router(product.router)
app.include_router(authentication.router)

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
# allow origins = 허용할 주소
# allow credential = 사용자 인증 정보(쿠키, 인증 헤더)를 포함할 지 여부
# allow methods = 허용할 HTTP 메서드 목록 ["GET", "POST"]
# allow headers = 허용할 HTTP 헤더의 목록
app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"]
)


# Token
# verify token
# retrieve user associated with token
# secure more endpoints

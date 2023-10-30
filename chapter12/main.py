from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse, PlainTextResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.websockets import WebSocket
from router import blog_get, blog_post, user, article, product, file 
from auth import authentication
from templates import templates
from db import models
from db.database import engine
from exceptions import StoryException
import time
from client import html
# uvicorn main:app --reload

# async await
# 비동기(병렬 처리)
# I/O 작업이나 네트워크 호출 등의 시간이 걸리는 작업 처리하는데 유용

# Templates
# real time HTML Editor
# https://htmledit.squarefree.com/

# webSockets
# two way communication
# keep connection open

app = FastAPI()
app.include_router(templates.router)
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


@app.get("/")
async def get():
    return HTMLResponse(html)
clients = []
@app.websocket("/chat")
# 웹소켓 연결을 처리
async def websocket_endpoint(websocket: WebSocket):
    # websocket 연결을 수락하는 비동기 함수
    await websocket.accept()
    # 연결된 client 기록
    clients.append(websocket)
    
    while True:
        # client가 준 text를 받는다.
        data = await websocket.receive_text()
        # 연결되어있는 모든 client에게 text를 보낸다.
        for client in clients:
            await client.send_text(data)
# 모든 HTTP 요청에 대해 호출되는 미들웨어 함수
# api를 호출할 때 걸리는 처리 시간 확인
# 클라이언트가 요청을 보내면 middleware에서 먼저 받은 후 api router로 넘긴다.
# call_next(request) - 클라이언트의 요청 처리 -> 실행시간 response의 headers에 붙임
@app.middleware("http")
async def add_middleware(request:Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    duration = time.time() - start_time
    response.headers['duration'] = str(duration)
    return response

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

# DB 변경을 원하면 생성된 db 파일 삭제
models.Base.metadata.create_all(engine)


# localhost:8000/files/fubao1.jpg
# Fastapi 내부에서 정적 파일(HTML, CSS, 이미지 파일 등)서비스하거나 관리할 수 있다. 
app.mount("/files", StaticFiles(directory="files"), name="files")
app.mount("/templates/static", 
          StaticFiles(directory="templates/static"),
            name= "static"
        )
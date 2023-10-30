from fastapi import APIRouter
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.requests import Request
from schemas import ProductBase
from custom_log import log
from fastapi import BackgroundTasks
router = APIRouter(
    prefix = "/templates",
    tags = ["templates"]
)
# Jinja2Templates html에서 {}, {{}} 을 사용해서 python에서 프로그래밍 가능
template = Jinja2Templates(directory="templates")

@router.post("/products/{id}", response_class=HTMLResponse)
def get_product(id:str, product: ProductBase, request: Request, bt: BackgroundTasks):
    # background task
    # 백그라운드에서 비동기적으로 실행
    # ex. 요청 처리하면서 데이터베이스에 로그 기록, 이메일 전송 작업
    bt.add_task(log_template_call, f"Template read for product with id : {id}")
    # request = 클라이언트 요청과 관련된 정보를 제공
    # HTML 템플릿 응답 생성
    # 템플릿 파일명 < 변수들 전달
    return template.TemplateResponse(
        "product.html",
        {
            "request": request,
            "id" : id,
            "title": product.title,
            "description": product.description,
            "price" : product.price
        }
    )

def log_template_call(message: str):
    log("MyAPI", message)
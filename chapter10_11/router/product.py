from fastapi import APIRouter, Header, Cookie, Form
from fastapi.responses import Response, HTMLResponse, PlainTextResponse
from typing import Optional, List
from custom_log import log
router = APIRouter(
    prefix = '/product',
    tags = ['product']
)

products = ['watch', 'camera', 'phone']
# Form(...) 필수로 작성해야 하는 데이터.
@router.post('/new')
def create_product(name: str = Form(...)):
    products.append(name)
    return products

@router.get('/all')
def get_all_products():
    log("MyAPI", "Call to get all products")
    # return products
    data = " ".join(products)
    response = Response(content= data, media_type='text/plain')
    response.set_cookie(key="test_cookie", value = "test_cookie_value")
    return response
# 왜 Response를 사용하는가 
# add parameters(headers, cookies, response type ...)
# different types of response(plain text, xml, html, files, streaming)
# better docs

# custom header는 개발자모드에서 볼 수 있다. network -> headers
@router.get('/withheader')
def get_products(response: Response,
                 custom_header: Optional[List[str]] = Header(None),
                 test_cookie: Optional[str] = Cookie(None)
                 ):
    if custom_header:
        response.headers['custom_response_header'] = " and ".join(custom_header)
        return { 
            'data': products,
            'custom_header': custom_header,
            'my_cookie': test_cookie}
# API endpoint 응답에 대한 문서화와 스펙을 정의
# API 사용자 및 개발자에게 API의 동작과 응답 형식에 대한 정보 제공
@router.get('/{id}', responses = {
    200:{
        "content":{
            "text/html" : {
                "example" : "<div>Product</div>"
            }
        },
        "description" : "Return the HTML for an object"
    },
    404: {
        "content":{
            "text/plain" : {
                "example" : "Product not available"
            }
        },
        "description" : "Acleartext error message"
    }
})
def get_product(id: int):
    if id > len(products):
        out = "Product not available"
        return PlainTextResponse(status_code=404, content= out, media_type="test/plain")
    
    else:

        product = products[id]
        out = f"""
            <head>
                <style>
                -product {{
                width : 500px;
                height : 30px;
                border: 2px inset green;
                background-color: lightblue;
                text-align: center;
                }}
                </style>
            </head>
            <dev class = "product">{product}</div>
            """
        return HTMLResponse(content=out, media_type="text/html")
    

    # cookies
    # store information on the browser
    # str, list, dict, models

    # Cross Origin Resource Sharing
    # localhost:8080<-->localhost:8000
    # origin 웹페이지, 도메인에서 다른 도메인을 가진 리소스에 접근하는 보안 메커니즘
    # 원래는 동일한 출처의 리소스만 접근하도록 제한됨(프로토콜, 호스트명, 포트가 같은 것)
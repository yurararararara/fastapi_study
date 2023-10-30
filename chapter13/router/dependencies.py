from fastapi import APIRouter
from fastapi.requests import Request
from fastapi.param_functions import Depends
from custom_log import log
router = APIRouter(
    prefix = "/dependencies",
    tags= ["dependencies"],
    dependencies=[Depends(log)]
)
# Depends
# 의존성 주입
# 모듈화, 함수 재사용
# 테스트 용이
def convert_params(request: Request, separator: str):
    query = []
    # url에 포함된 query parameter
    for key, value in request.query_params.items():
        query.append(f"{key} {separator} {value}")
    return query

def convert_headers(request: Request, separator: str = "--", query = Depends(convert_params)):
    out_headers = []
    # Http 요청의 헤더 정보
    for key, value in request.headers.items():
        out_headers.append(f"{key} {separator} {value}")

    return {
        "headers" : out_headers,
        'query' : query
        }


@router.get('')
def get_items(test : str, separator: str = "--", headers = Depends(convert_headers)):
    return{
        "items" : ["a", "b", "c"],
        "headers" : headers
    }


@router.post("/new")
def create_item(headers = Depends(convert_headers)):
    return {
        "result" : "new item created",
        "headers" : headers
    }


class Account:
    def __init__(self, name: str, email: str):
        self.name = name
        self.email = email
        
@router.post("/user")
# 받은 name, email 값은 Account 클래스에 사용
def create_user(name: str, email: str, account : Account = Depends()):
    return {
        "name" : account.name,
        "email" : account.email
    }


# Multi level dependencies
# dependencies can have dependencies


# Global dependencies
# Apply to * all endpoints
# router
# app
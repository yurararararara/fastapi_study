from fastapi import APIRouter, status, Response
from enum import Enum
from typing import Optional
# tag = documentation을 구조화
# prefix = 공통 경로
router = APIRouter(
    prefix= "/blog",
    tags = ["blog"]
)
# 1
# summary = 짧은 설명
# description = 마크다운 텍스트 포함 -> 긴 설명
# response_description = 상태 코드에 대한 예상 응답 모델 설명
@router.get(
        "/all",
         summary='Retrieve all blogs',
         description='This api call simulates fetching all blogs',
         response_description="The list of available blogs"
         )

def get_all_blogs(page = 1, page_size : Optional[int] = None):
    # return {"message" : "All blogs provided"}
    return {"message" : f"All {page_size} blogs on page {page}"}

# 2
# Predefined values with Enum
class BlogType(str, Enum):
    short = 'short'
    story = 'story'
    howto = 'howto'

@router.get("/type/{type}")
def blog_type(type : BlogType):
    return {"message" : f"Blog type : {type}"}
# 3
@router.get('/{id}/comments/{comment_id}', tags=['comment'])
def get_comment(id : int, comment_id : int, valid : bool = True, username : Optional[str] = None):
    """
    Simulates retrieving a comment of a blog

    - **id** mandatory path parameter
    - **comment_id** mandatory path parameter
    - **valid** optional query parameter
    - **username** optional query parameter
    """
    return {"message" : f"blog_id {id}, comment_id {comment_id}, valid {valid}, username {username}"}
# 4
# status code 지정 방법 두가지
# 오류 처리
# @router.get('/blog/{id}', status_code=404)
# @router.get('/blog/{id}', status_code=status.HTTP_200_OK)
@router.get('/{id}', status_code=status.HTTP_200_OK, tags=['blog'])
def get_blog(id : int, response : Response):
    if id > 5 : 
        response.status_code = status.HTTP_404_NOT_FOUND
        return {'error': f"Blog {id} not found"}
    else:
        response.status_code = status.HTTP_200_OK
        return {"message" : f"Blog with id {id}"}
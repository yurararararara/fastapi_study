from fastapi import APIRouter, Query, Path, Body
from typing import Optional, List, Dict
from pydantic import BaseModel

router = APIRouter(
    prefix = '/blog',
    tags = ['blog']
)
# pandantic model
# 데이터 유효성 검사 및 직렬화 모델로 사용
# Type hint를 사용해서 각 변수의 데이터 유형 결정
class Image(BaseModel):
    url: str
    alias: str

class BlogModel(BaseModel):
    title : str
    content: str
    nb_comment : int
    published : Optional[bool]
    tags: List[str] = []
    metadata: Dict[str, str] = {"key1": "val1"}
    image: Optional[Image] = None
    
@router.post('/new')
def create_blog(blog : BlogModel):
    # blog.title
    return {"data" : blog}

# path and query parameter
@router.post('/new/{id}')
def create_blog(blog: BlogModel, id: int, version: int = 1):
    return {
        'id' : id,
        "data" : blog,
        'version' : version
        }

# parameter metadata
# Information displayed in docs
# using the Query, path and Body imports
# content : str = Body() 괄호 안에 default value : 내용 넣기,non-optional parameters:  ... 또는 Ellipsis 
# Ellipsis는 줄임표(...)와 같은 역할.

# Body는 요청 본문에서 예상되는 매개변수를 정의하는데 사용, 리소스를 생성하거나 업데이트하는데 사용
# Query, path 둘다 문자열 길이와 숫자도 제한 할 수 있다. 
# Path는 경로의 일부인 매개변수를 정의하는데 사용, fastapi가 url에서 값을 추출하고 지정된 데이터 유형 및 유효성 검사를 하여 분석
# Query는 URL에서 쿼리 문자열의 일부인 매개 변수를 정의하는데 사용
# alias, deprecated는 Query 매개 변수에 대한 자세한 정보를 제공하는 추가 메타데이터 옵션, api 사용자에게 매개변수의 목적과 사용법을 문서화하고 전달하는 역할 
# deprecated는 Query 매개변수를 더이상 사용되지 않는 것을 표시. 향후 버전의 API에서 제거될 수 있음을 알리는 신호 역할.

@router.post('/new/{id}/comment/{comment_id}')
def create_comment(blog: BlogModel, id : int,
                comment_title: int = Query(None,
                    title = 'title of the comment',
                    description='Some description for comment_title',
                    alias = 'commentTitle',
                    deprecated=True
                ),
                content : str = Body(...,
                    min_length= 10,
                    max_length=50,
                    regex='^[a-z\s]*$'
                    ),
                v: Optional[List[str]] = Query(['1.0', '1.1', '1.2']),
                comment_id : int = Path(..., gt=5, le=10)
    ):
    return {
        'blog': blog,
        'id': id,
        'comment_title': comment_title,
        'content' : content,
        'version' : v,
        'comment_id': comment_id
        }

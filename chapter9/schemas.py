from pydantic import BaseModel
from typing import List
    
# Schema definition
# 외부로 공개되면 안되는게 있고, 출력값이 정확한지 검증도 해야 함으로 추가적인 코딩
# User에게 받는 type of data 
class UserBase(BaseModel):
    username: str
    email: str
    password: str
# orm_mode = dict 자료형처럼 값을 읽게 해줌. article.title
# Article inside UserDisplay
class Article(BaseModel):
    title : str
    content : str
    published : bool
    class Config():
        # pydantic 버전 2에서는 orm_mode 대신 from_attriubtes 사용
        from_attributes = True
        # pydantic 버전이 2 이전일 때,
        # orm_mode = True

# user에게 보여주는 정보
class UserDisplay(BaseModel):
    username: str
    email: str
    items : List[Article] = []
    class Config():
        from_attributes = True

# User inside ArticleDisplay
class User(BaseModel):
    id : int
    username : str
    class Config():
        from_attributes = True

# user한테 받는 Article 정보
class ArticleBase(BaseModel):
    title : str
    content : str
    published : bool
    creator_id : int
# user에게 보여주는 정보
class ArticleDisplay(BaseModel):
    title: str
    content: str
    published : bool
    user : User
    class Config():
        from_attributes = True
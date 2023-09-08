from sqlalchemy.sql.sqltypes import Integer, String, Boolean
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.orm import relationship
from db.database import Base
from sqlalchemy import Column
# Model definition
# Create tables
# Table 2개 생성
# back_populates는 cascading options
# mysql에서 on update cascade, on delete cascade와 동일하다.
# 데이터의 일관성을 위함.
class DbUser(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key = True, index = True)
    username = Column(String)
    email = Column(String)
    password = Column(String)
    items = relationship("DbArticle", back_populates = '')

class DbArticle(Base):
    __tablename__ = 'articles'
    id = Column(Integer, primary_key = True, index = True)
    title = Column(String)
    content = Column(String)
    published = Column(Boolean)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("DbUser", back_populates = 'items')
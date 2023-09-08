from fastapi.security import OAuth2PasswordBearer
from typing import Optional
from datetime import datetime, timedelta
# json web token
from jose import jwt
from jose.exceptions import JWTError
from fastapi.param_functions import Depends
from sqlalchemy.orm import Session
from db.database import get_db
from fastapi import HTTPException, status

from db import db_user
#  토큰을 얻는 endpoint
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
# jwt토큰을 생성하고 디코드할 때 사용
# 토큰의 암호화 및 검증에 사용
SECRET_KEY = '77407c7339a6c00544e51af1101c4abb4aea2a31157ca5f7dfd87da02a628107'
# 토큰의 암호화 알고리즘
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30
 
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
  to_encode = data.copy()
  if expires_delta:
    expire = datetime.utcnow() + expires_delta
  else:
    expire = datetime.utcnow() + timedelta(minutes=15)
  # 만료시간을 데이터에 추가한다.
  to_encode.update({"exp": expire})
  encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
  return encoded_jwt

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
  credential_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail = "Could not validate credentials",
    headers = {"www-Authenticate": "Bearer"}
  )
  try:
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    username: str = payload.get("sub")
    if username is None:
      raise credential_exception
  except JWTError:
    raise credential_exception
  
  user = db_user.get_user_by_username(db, username)
  if user is None:
    raise credential_exception
  return user
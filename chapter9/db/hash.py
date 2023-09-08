from passlib.context import CryptContext
# passlib는 Hash 관련 라이브러리
pwd_cxt = CryptContext(schemes = 'bcrypt', deprecated = 'auto')

class Hash():
    # 해시된 암호를 반환
    def bcrypt(password: str):
        return pwd_cxt.hash(password)
    # 입력된 password와 저장되어있는 해시 값이 동일한지 확인
    def verify(hashed_password, plain_password):
        return pwd_cxt.verify(plain_password, hashed_password)
from sqlalchemy.orm.session import Session
from schemas import UserBase
from db.models import DbUser
from db.hash import Hash
# create functionality to write to database
# Session은 CRUD 작업을 수행하는 메서드 제공(상호작용)
def create_user(db: Session, request: UserBase):
    new_user = DbUser(
        username = request.username,
        email = request.email,
        password = Hash.bcrypt(request.password)
    )
    # Dbuser 인스턴스를 Session에 추가
    db.add(new_user)
    # DB에 변경 사항을 커밋
    db.commit()
    # new_user 인스턴스를 DB와 동기화
    # get the ID to our new user
    db.refresh(new_user)
    return new_user

def get_all_users(db: Session):
    return db.query(DbUser).all()

def get_user(db: Session, id: int):
    # Handle any exception
    return db.query(DbUser).filter(DbUser.id == id).first()
    # 조건을 추가하고 싶을 때
    # return db.query(DbUser).filter(DbUser.id == id).filter(DbUser.email == email).first()


def update_user(db: Session, id: int, request : UserBase):
    user = db.query(DbUser).filter(DbUser.id == id) 
    # Handle any exception
    user.update({
        DbUser.username : request.username,
        DbUser.email : request.email,
        DbUser.password : Hash.bcrypt(request.password)
    })
    db.commit()
    return "ok"

def delete_user(db: Session, id: int):
    user = db.query(DbUser).filter(DbUser.id == id).first()
    # Handle any exception
    db.delete(user)
    db.commit()
    return "ok"

# retrieve elements from multple tables in a single request

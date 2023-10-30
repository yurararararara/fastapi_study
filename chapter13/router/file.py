from fastapi import APIRouter, File, UploadFile
import shutil
from fastapi.responses import FileResponse

router = APIRouter(
    prefix = "/file",
    tags= ['file']
)
# 업로드한 파일의 내용 읽기
# File : 입력 필드 타입, 클라이언트가 서버에 파일을 업로드할 때 사용.
@router.post('/file')
def get_file(file:bytes = File(...)):
    content = file.decode("utf-8")
    lines = content.split("\n")
    return {"lines" : lines}
# 업로드한 파일의 파일명 읽기
# uploadfile : 클라이언트가 업로드한 파일을 서버에서 쉽게 다루기 위한 도구
# 최대 크기 제한까지만 메모리에 저장, 초과하면 디스크에 저장
# 대용량 파일을 처리하기에 적합
# async await
@router.post("/uploadfile")
def get_upload_file(upload_file: UploadFile = File(...)):
    path = f"files/{upload_file.filename}"
    # 업로드한 파일을 복사한다.
    with open(path, "w+b") as buffer:
        shutil.copyfileobj(upload_file.file, buffer)

    return {
        'filename' : upload_file.filename,
        'type' : upload_file.content_type 
    }
# FileResponse는 파일 다운로드를 위해 사용. 클라이언트에게 파일을 응답으로 전송할때.

@router.get("/download.{name}", response_class = FileResponse)
def get_file(name: str):
    path = f"img/{name}"
    return path
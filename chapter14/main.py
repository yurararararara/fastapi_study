from fastapi import FastAPI, File, UploadFile
import shutil
import pytesseract
# uvicorn main:app --reload
app = FastAPI()
# OCR
# third party library use -> confidence
# bragging rights

@app.post("/ocr")
# ... 해당 필드가 필수적으로 제공되어야 함. 
def ocr(image: UploadFile = File(...)):
    filePath = "txtFile"
    with open(filePath, "w+b") as buffer : 
        shutil.copyfileobj(image.file, buffer)

    return pytesseract.image_to_string(filePath, lang ="eng")
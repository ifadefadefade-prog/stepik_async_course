from typing import Annotated, List
from fastapi import FastAPI, File, UploadFile


app = FastAPI()


#загружает только содержимое файла в видек bytes в оперативную память,
#хорошо для небольших файлов
@app.post('/files/')
async def create_file(file: Annotated[bytes, File()]):
    return {'file_size': len(file)}


#использует временные фалы, дает доступ к матеинформации файла
#такой как имя, тип(file.content_type) и методы file.read()
#позволяет читаьь файлы целиком
@app.post('/uploadfile/')
async def create_upload_file(file: UploadFile):
    content = await file.read()
    return {'filename': file.filename, 'size': len(content)}


#позволяет читаnь файлы частями
@app.post('/uploadfile/')
async def create_upload_file(file: UploadFile):
    with open(file.filename, 'wb') as f:
        while chunk := await file.read(1024):
            f.write(chunk)

    return {'filename': file.filename}


@app.post('/multiple-files/')
async def upload_multiple_files(files: List[UploadFile]):
    return {"filenames": [file.filename for file in files]}


#мы можем делать ограничения по загрузке типов файлов
#ниже пример с изображениями
@app.post('/multiple-image/')
async def upload_image(file: UploadFile):
    if file.content_type not in ["image/jpeg", "image/png"]:
        return {"error": "Только JPG и PNG разрешены"}
    return {"filename": file.filename, "content_type": file.content_type}
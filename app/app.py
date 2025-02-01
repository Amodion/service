from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import File, UploadFile, Request, FastAPI, HTTPException
from typing import Annotated
from ml import detect, detect_files
import sys

app = FastAPI()

templates = Jinja2Templates(directory="./app/static/templates")

@app.get('/')
async def root(request: Request):
    return templates.TemplateResponse(
        request=request, name='index.html'
    )

# Принимает чистые байты, теряются метаданные на подобии имени
@app.post("/upload", deprecated=True)
async def upload(request: Request, files: Annotated[list[bytes], File(...)]):
    try:                                                   
        contents = files
    except Exception:
        raise HTTPException(status_code=500, detail='Something went wrong')

    context = await detect_files(contents)
        
    return templates.TemplateResponse(request=request,
                                        name="index.html",
                                        context=context)

# Принимает объекты типа UploadFile, это лучше и надежднее чистых байтов. Позволяет сохранять метаданные.
@app.post("/uploadfiles")
async def upload(request: Request, files: Annotated[list[UploadFile], File(...)]):
    files_validation(files)
    try:                                                   
        contents = files
    except Exception:
        raise HTTPException(status_code=500, detail='Something went wrong')

    context = await detect_files(contents)
        
    return templates.TemplateResponse(request=request,
                                        name="index.html",
                                        context=context)

# Проверяет, что на вход пришли изображения поддерживаемых фомратов
def files_validation(files: list[UploadFile]):
    for file in files:
        MIME_type, media_type = file.content_type.split('/')
        if MIME_type != 'image':
            raise HTTPException(500, detail="Принимаются только изображения!")
        elif media_type not in ['jpg', 'jpeg', 'png']:
            raise HTTPException(500, detail="Принимаются только изображения форматов '.jpg', '.jpeg', '.png'!")
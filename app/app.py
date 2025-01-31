from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import File, UploadFile, Request, FastAPI, HTTPException
import cv2
import numpy as np
import base64
from io import BytesIO
from PIL import Image

app = FastAPI()

app.mount("/static", StaticFiles(directory="./app/static"), name="static")


templates = Jinja2Templates(directory="./app/static/templates")

@app.get('/')
async def root(request: Request):
    return templates.TemplateResponse(
        request=request, name='index.html'
    )

@app.post("/upload")
async def upload(request: Request, file: UploadFile = File(...)):
    try:                                                   
        contents = file.file.read()
    except Exception:
        raise HTTPException(status_code=500, detail='Something went wrong')
    finally:
        file.file.close()

    nparr = np.fromstring(contents, np.uint8)
    img_np = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    result_img = cv2.flip(img_np, 0)                    # ТУТ ПРЕОБРАЗОВВАНИЯ С КАРТИНКАМИ (ТУТ БУДЕТ РАБОТАТЬ ML МОДЕЛЬ)
    #cv2.imwrite('flipped_' + file.filename, result_img)
    
    result_img = cv2.cvtColor(result_img, cv2.COLOR_BGR2RGB)
    im = Image.fromarray(result_img)

    buffer = BytesIO()
    im.save(buffer, format='jpeg')
    encoded_image = base64.b64encode(buffer.getvalue()).decode("utf-8")
        
    return templates.TemplateResponse(  request=request,
                                        name="display.html",
                                        context={   'image_name': file.filename,
                                                    "myImage": encoded_image})
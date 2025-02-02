from typing import List
import cv2
import numpy as np
import base64
from io import BytesIO
from PIL import Image
from fastapi import UploadFile
from ultralytics import YOLO

async def detect(images: List[bytes]):
    return_images = []                                      
    
    for file in images:
        nparr = np.fromstring(file, np.uint8)
        img_np = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        result_img = cv2.flip(img_np, 0)                    # ТУТ ПРЕОБРАЗОВВАНИЯ С КАРТИНКАМИ (ТУТ БУДЕТ РАБОТАТЬ ML МОДЕЛЬ)
    #cv2.imwrite('flipped_' + file.filename, result_img)
    
        result_img = cv2.cvtColor(result_img, cv2.COLOR_BGR2RGB)
        im = Image.fromarray(result_img)

        buffer = BytesIO()
        im.save(buffer, format='jpeg')
        encoded_image = base64.b64encode(buffer.getvalue()).decode("utf-8")
        return_images.append({'bytes': encoded_image,
                              'bboxes': [[1, 2, 3], [4, 5, 6]]})

    return {'data': return_images}

async def detect_files(images: List[UploadFile]):
    return_images = []
    model = YOLO("./weights/yolo11n-custom.pt")          # Добавить определение устройства                            
    
    for file in images:
        # создание привычного numpy массива изображения
        img = file.file.read()
        nparr = np.fromstring(img, np.uint8)
        img_np = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        # работа с изображением
        #result_img = cv2.flip(img_np, 0)
        result = model.predict(img_np, verbose=False)[0]  # detect only cars
        boxes = result.boxes.xyxy.detach().cpu().numpy()
        result_img = result.plot()                
    
        # перевод numpy массива в байты для отображения. Без BitesIO были проблемы с отобажением
        result_img = cv2.cvtColor(result_img, cv2.COLOR_BGR2RGB)
        im = Image.fromarray(result_img)
        buffer = BytesIO()
        im.save(buffer, format='jpeg')
        encoded_image = base64.b64encode(buffer.getvalue()).decode("utf-8")

        return_images.append({'bytes': encoded_image,
                              'bboxes': f'Bboxes изображения {file.filename}: {boxes}'})

    return {'data': return_images}
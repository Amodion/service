# 
FROM python:3.12

# 
WORKDIR /app

# 
COPY ./requirements.txt /app/requirements.txt

# 
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt
RUN apt-get update && apt-get install libgl1 -y

# 
COPY ./app /app/app
COPY ./weights /app/weights

# 
CMD ["sh", "-c", "fastapi run app/app.py --host $APP_IP --port $APP_PORT"]
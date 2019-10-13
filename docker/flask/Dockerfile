FROM python:3.7-rc-slim
COPY app /app

WORKDIR /app

RUN pip install -r requirements.txt

CMD ["python", "app_restful.py"]

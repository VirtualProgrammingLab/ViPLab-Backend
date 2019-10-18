FROM python:3.7-rc-slim
COPY app /app

WORKDIR /app

RUN pip install -r requirements.txt

RUN chmod +x run.sh

CMD [./run.sh]

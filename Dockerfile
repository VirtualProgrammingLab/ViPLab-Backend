FROM python:3.8-alpine

LABEL maintainer="pascal.seeland@tik.uni-stuttgart.de"

WORKDIR /

COPY requirements.txt ./

RUN apk add --no-cache libmagic cyrus-sasl openssl

RUN apk add --no-cache --virtual .build-deps  \
		gcc \
#		libffi-dev \
 		musl-dev \
		openssl-dev \
cyrus-sasl-dev\
        
  &&  pip install --no-cache-dir -r requirements.txt \
  &&   apk del --no-network .build-deps 


COPY backend.py amqp_messager.py models.py /
COPY config.ini /

ENV PYHTONPATH /
ENTRYPOINT [ "python" ]

CMD [ "backend.py"]

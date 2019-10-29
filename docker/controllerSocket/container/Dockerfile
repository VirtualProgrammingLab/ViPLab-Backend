FROM python

RUN pip install --upgrade pip

COPY requirements.txt ./

COPY kata_socket_server.py ./

RUN pip install -r requirements.txt

RUN apt-get update

#RUN apt-get install gcc

RUN apt-get install vim -y

ENTRYPOINT [ "python" ]

CMD [ "kata_socket_server.py" ]


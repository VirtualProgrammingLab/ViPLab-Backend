FROM python

RUN pip install --upgrade pip

COPY /intoContainer ./

#COPY ./intoContainer/kata_socket_server.py ./

#WORKDIR /home

RUN pip install -r requirements.txt

RUN apt-get update

#RUN apt-get install gcc

RUN apt-get install vim -y

ENTRYPOINT [ "python" ]

CMD [ "kata_socket_server.py" ]


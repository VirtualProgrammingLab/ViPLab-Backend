FROM gcc 

RUN apt-get update

RUN apt-get install python3

RUN apt-get install python3-pip -y

RUN pip3 install --upgrade pip

COPY /intoContainer ./

#COPY ./intoContainer/kata_socket_server.py ./

#WORKDIR /home

RUN pip3 install -r requirements.txt

#RUN apt-get update

#RUN apt-get install gcc

#RUN apt-get install vim -y

ENTRYPOINT [ "python3" ]

CMD [ "kata_socket_server.py" ]


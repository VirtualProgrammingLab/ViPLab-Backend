FROM python

#COPY resolv.conf ./etc/resolv.conf
RUN pip install --upgrade pip

COPY requirements.txt ./

COPY server.py ./


RUN pip install -r requirements.txt

RUN apt-get update

#RUN apt-get install gcc

RUN apt-get install vim -y

ENTRYPOINT [ "python" ]

CMD [ "server.py" ]

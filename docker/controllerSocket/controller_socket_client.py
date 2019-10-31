'''
@autor: Julia
'''
import docker
import requests
from flask import Flask, request
from flask_restful import Resource, Api
import json
import socket
import sys
import time
import findLanguage
import struct


app = Flask(__name__)
api = Api(app)
client= docker.from_env()

class results(Resource):
	def post(self):
                input=json.loads(request.stream.read())
                findLanguage.printResult(json.dumps(input))
		#return {"The result is: " : input}, 201

class startingNewContainer(Resource):

    def startContainer(self, language):
        containerObject = client.containers.run("python_socket_" + language + "_test", runtime="kata-fc", publish_all_ports=True, detach=True, stdin_open=True)
        a = True
        containerId= vars(containerObject)["attrs"]["Id"]
        while a==True:
            container=client.containers.get(containerId)
            containerIp = vars(container)["attrs"]["NetworkSettings"]["Networks"]["bridge"]["IPAddress"]
            if containerIp!="":
                a=False
        print(containerIp)
        return containerIp


    def openSocket(self, ip, data):
        port=5005
        server_address = (ip, port)
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        time.sleep(5)
        client_socket.connect(server_address)
        data_in_bytes = json.dumps(data).encode("utf-8")
        amount_data = sys.getsizeof(data_in_bytes)        
        client_socket.send(str(amount_data).encode("utf-8")) 
        time.sleep(0.5)
        client_socket.sendall(data_in_bytes)
        return 200
        #return client_socket.recv(amount_data).decode("utf-8")

    
    def post(self):
        input=json.loads(request.stream.read())
        language = input["language"].lower()
        data = input["data"]
        ip = self.startContainer(language)
        return self.openSocket(ip, data)
        

api.add_resource(results,'/results')
api.add_resource(startingNewContainer,'/newcontainer')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)

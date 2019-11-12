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
                print(json.dumps(input,  indent=4))
                #findLanguage.printResult(json.dumps(input))
		#return {"The result is: " : input}, 201

class startingNewContainer(Resource):

    def startContainer(self, language, debug):
        containerObject = client.containers.run("gcc_python_socket_" + language, runtime="kata-fc", publish_all_ports=True, auto_remove=debug, detach=True, stdin_open=True)
        a = True
        containerId= vars(containerObject)["attrs"]["Id"]
        while a==True:
            container=client.containers.get(containerId)
            containerIp = vars(container)["attrs"]["NetworkSettings"]["Networks"]["bridge"]["IPAddress"]
            if containerIp!="":
                a=False
        print(containerIp)
        return containerIp, containerId


    def openSocket(self, ip, data):
        port=5005
        server_address = (ip, port)
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        connected = False
        while not connected:
            try:
                client_socket.connect(server_address)
                connected = True
            except Exception as e:
                pass
        #time.sleep(5)
        #client_socket.connect(server_address)
        data_in_bytes = json.dumps(data).encode("utf-8")
        amount_data = sys.getsizeof(data_in_bytes)        
        client_socket.send(str(amount_data).encode("utf-8")) 
        time.sleep(0.25)
        client_socket.sendall(data_in_bytes)
        return 200
        #return client_socket.recv(amount_data).decode("utf-8")

    
    def post(self):
        #conf_file = open("./examples/config.json")
        #config = json.load(conf_file)
        #conf_file.close()
        input=json.loads(request.stream.read())
        language = input["language"].lower()
        data = input["data"]
        debug = input["debug"]
        #whole_data = {"data": data, "receiver": input["receiver"], "conf":config}
        whole_data = {"data": data, "receiver": input["receiver"]}
        ip, container_id = self.startContainer(language, debug)
        statuscode = self.openSocket(ip, whole_data)
        return {container_id:input.get("receiver")}, statuscode
        

api.add_resource(results,'/results')
api.add_resource(startingNewContainer,'/newcontainer')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)

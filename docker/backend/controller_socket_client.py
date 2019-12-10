'''
@autor: Julia
This is the backend of the proof of concept container managed VipLab.
This flask server provides two endpoints:
    - /newcontainer: starts a new container from the corresponding language image, opens a socket, pushes the needed data through and closes the socket.
    - /results: takes the computed results from the container and pushes it back to the ECS.
'''

import docker
import requests
from flask import Flask, request
from flask_restful import Resource, Api
import json
import socket
import time
import sys

app = Flask(__name__)
api = Api(app)
client= docker.from_env()

class results(Resource):
	def post(self):
            '''
            Endpoint to push results from the container to the flask backend server. -> POST result to ECS Server
            Method: POST
            Data: '{"Result": result, "receiver": receiver}'
            '''
            input=json.loads(request.stream.read())
            receiver = input.get("receiver")
            result = input.get("Result")
            r = requests.post('https://nfldevvipecs.rus.uni-stuttgart.de/numlab/results', headers={'X-EcsReceiverMemberships':receiver,'Accept': 'application/json', "Content-Type":"application/json"}, data=json.dumps(result), auth=("pinfcc2", "YqYsyjVLomICGTY7SK6e"))
            print(r.headers)
            print(r.status_code)
            print(json.dumps(input,  indent=4))
                

class startingNewContainer(Resource):

    def startContainer(self, language, debug):
        '''
        starts a kata container
        Params:
        - language (string): programming language from the code which has to be compiled
        - debug (bool): decides if the container is removed after compiling sucessfully (debug=True), or if the container will not be removed after compiling sucessfully (debug=False)
        Return:
        - ip of started container 
        - id of started container
        '''
        containerObject = client.containers.run("python_socket_" + language, runtime="kata-fc", publish_all_ports=True, auto_remove=debug, detach=True, stdin_open=True)
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
        '''
        opens a socket into the started container
        Params:
        - IP Address of corresponding container
        - data (json/dict): data which has to be transfered into the container
        Return:
        201: if everything went good
        500: if something went wrong
        '''
        try:
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
            data_in_bytes = json.dumps(data).encode("utf-8")
            amount_data = sys.getsizeof(data_in_bytes)        
            client_socket.send(str(amount_data).encode("utf-8")) 
            time.sleep(0.01)
            client_socket.sendall(data_in_bytes)
            return 201
        except:
            return 500
        

    def post(self):
        '''
        Endpoint of /newcontainer
        Method: POST
        Data: '{"language":language, "data":data, "debug": debug, "receiver":receiver}'
        Return:
        - dict: '{"container_id": receiver}'
        - statuscode from openSocket
        '''
        #conf_file = open("/home/julia/backend/examples/config.json")
        #config = json.load(conf_file)
        #conf_file.close()
        config = {"timelimitInSeconds": 15}
        input=json.loads(request.stream.read())
        language = input["language"].lower()
        if language != "c":
            return {0:0}, 400
        else:
            data = input["data"]
            debug = input["debug"]
            whole_data = {"data": data, "receiver": input["receiver"], "conf":config}
            ip, container_id = self.startContainer(language, debug)
            statuscode = self.openSocket(ip, whole_data)
            return {container_id:input.get("receiver")}, statuscode
        

api.add_resource(results,'/results')
api.add_resource(startingNewContainer,'/newcontainer')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)

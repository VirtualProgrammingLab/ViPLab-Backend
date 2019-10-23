'''
@autor: Julia
'''
import docker
import requests
from flask import Flask, request
from flask_restful import Resource, Api
import json
import time

app = Flask(__name__)
api = Api(app)
client= docker.from_env()

class results(Resource):
	def post(self):
		return {"the result is: " : request.get_json()}, 201

class startingNewContainer(Resource):
    
    def startContainer(self, language):
        global client
        containerObject = client.containers.run("python_flask_" + language, runtime="kata-fc", publish_all_ports=True, detach=True, stdin_open=True)
        containerId= vars(containerObject)["attrs"]["Id"]

        a = True
        while a==True:
            container=client.containers.get(containerId)
            containerIp = vars(container)["attrs"]["NetworkSettings"]["Networks"]["bridge"]["IPAddress"]
            if containerIp!="":
                a=False
        return containerIp

    def postDataToContainer(self, ip, data):
        url = "http://"+str(ip)+":5000/data"
        print(ip)
        datajson=json.dumps(data)
        
        b=True
        while b == True:
            try:
                response=requests.post(url, data=datajson, headers = {'Content-type':'application/json'})
                b = False
            except:
                pass
        
        
        '''
        response = None
        while response is None:
            try:
                response = requests.post(url, data=data, headers = {'Content-type': 'application/json'})
             
            except:
                pass
        
        time.sleep(1)
        try:
             response = requests.post(url, data=datajson, headers = {'Content-type': 'application/json'})

        except:
            time.sleep(1)
            response = requests.post(url, data=datajson, headers = {'Content-type': 'application/json'})

        #response = requests.post(url, data=data) 
        '''
        return response.json()
    
    def post(self):
        input=json.loads(request.stream.read())
        language = input["language"].lower()
        data = input["data"]
        ip = self.startContainer(language)
        output = self.postDataToContainer(ip, data)
        return output
        #return {"the language is: " : language, "data is:": data, "ip":ip}, 201

api.add_resource(results,'/results')
api.add_resource(startingNewContainer,'/newcontainer')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

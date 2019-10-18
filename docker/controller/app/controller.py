'''
@autor: Julia
'''
import docker
import requests
from flask import Flask, request
from flask_restful import Resource, Api
import json

app = Flask(__name__)
api = Api(app)
client= docker.from_env()

class results(Resource):
	def post(self):
		return {"the result is: " : request.get_json()}, 201

class startingNewContainer(Resource):
    
    def startContainer(self, language):
        containerObject = client.containers.run("python_flask_" + language, runtime="kata-fc", publish_all_ports=True, detach=True, stdin_open=True)
        #containerId= vars(containerObject)["attrs"]["Id"]
        containerIp = vars(containerObject)["attrs"]["NetworkSettings"]["Networks"]["bridge"]["IPAddress"]
        print(containerIp)
        return containerIp

    def postDataToContainer(self, ip, data):
        response = requests.post('https:'+ip+":5000/data", data=data)
        return response.status_code
    
    def post(self):
        input=json.loads(request.stream.read())
        language = input["language"].lower()
        data = input["data"]
        ip = self.startContainer(language)
        return self.postDataToContainer(ip, data)
        #return {"the language is: " : language, "data is:": data}, 201

api.add_resource(results,'/results')
api.add_resource(startingNewContainer,'/newcontainer')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
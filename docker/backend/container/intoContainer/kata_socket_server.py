'''
@autor Julia
Socketserver läuft in kata
'''
import socket
import json
import requests
import dataObjects
from c import C
import sys
import os
import subprocess

def computeResult(data):
    '''
    data = {Exercise, Solution}
    aus data werden Exercise und Solution Objekte erstellt
    erst Exercise Objekt erstellen und dann dem Solution Objekt übergeben (analog zur main)
    Solution Objekt muss Copiler übergeben werden -> Import language specific compiler file
    
        comp = C(solution)
        comp.processData()
        r = comp.result
        return r.createJson()

    dataObjects.py in Dockerfile einfügen

    '''
    #print("sys.argv[0]: " + sys.argv[0])
    #print("os.path.dirname(os.path.abspath(sys.argv[0])): " + os.path.dirname(os.path.abspath(sys.argv[0])))
    exercise = dataObjects.Exercise({"Exercise" : data["Exercise"]})
    solution = dataObjects.Solution({"Solution" : data["Solution"]}, exercise)
    comp = C(solution)
    comp.processData()
    return comp.result.createJson()


def sendResultsBackToController(result_json, receiver):
    #print(type(json.loads(result_json)))
    #print(result_json)
    #data = {"Result": json.loads(result_json).get("Result"), "receiver":receiver}
    #data_json = json.dumps(data)
    result_jsons = json.loads(result_json)
    result_jsons.update({"receiver":receiver})
    requests.post('http://172.17.0.1:5001/results', data=json.dumps(result_jsons), headers = {'Content-type': 'application/json'})


def startSocket():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    address_host = ("0.0.0.0", 5005) #IP Adresse von sich selbst 
    server_socket.bind(address_host)
    server_socket.listen(1)
    (client_socket, addr) = server_socket.accept()
    amount_data = int(client_socket.recv(512).decode("utf-8")) 
    data = json.loads(client_socket.recv(amount_data).decode("utf-8"))
    return data

if __name__ == '__main__':
    data = startSocket()
    real_data = data.get("data")
    receiver = data.get("receiver")
    #print(data)
    result = computeResult(real_data)
    print(result)
    sendResultsBackToController(result, receiver)
    

'''
@autor Julia
Socketserver läuft in kata
'''
import socket
import json
import requests

def computeResult(data):
    return True

def sendResultBackToController(result_json):
    requests.post('http://127.17.0.1:5001/results', data=result_json, headers = {'Content-type': 'application/json'})


def startSocket():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    address_host = ("0.0.0.0", 5005) #IP Adresse von sich selbst 
    server_socket.bind(address_host)
    server_socket.listen(1)
    (client_socket, addr) = server_socket.accept()
    amount_data = int(client_socket.recv(1024).decode("utf-8")) 
    data = json.loads(client_socket.recv(amount_data).decode("utf-8"))


    #client_socket.send(data.encode("utf-8"))
    #result_json = computeResult(data)
    #sendResultBackToController(result_json)


if __name__ == '__main__':
    startSocket()

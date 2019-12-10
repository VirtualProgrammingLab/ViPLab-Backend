import json
import socket



exercise = open("/home/julia/controller/app/examples/exercise.json")
data = json.load(exercise)

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

ip_address_kata = '172.17.0.2' #hier kommt die IP vom kata container
port = 5005
server_address = (ip_address_kata, port)

client_socket.connect(server_address)

client_socket.sendall(json.dumps(data).encode("utf-8"))

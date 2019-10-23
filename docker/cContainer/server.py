from flask import Flask, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

class HelloWorld(Resource):
    def post(self):
        data = request.get_json()
        computeSolution(data)
        return 200

def computeSolution(data):
    ''' dies ist die Methode, die das Ergebnis berechnet'''
    solution = data
    request.post('http://127.17.0.1:5000/results', data=solution, headers = {'Content-type': 'application/json'})
    
api.add_resource(HelloWorld, '/data')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

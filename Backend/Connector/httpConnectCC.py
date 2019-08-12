'''
@author: Joshua
'''
import json
import requests


class ConnectCC:
    '''
    classdocs
    '''
    user = ""
    pw = ""
    url = 'https://nfldevvipecs.rus.uni-stuttgart.de'
    def __init__(self , user , pw):
        self.user = user
        self.pw = pw

    def GetSolutions(self):
        print("GetSolution Start...")
        r = requests.post(self.url + '/numlab/solutions/fifo', auth=(self.user, self.pw))
        print(r.status_code)
        print(r.text)
        return True
        
    def GetExerciseList(self):
        print("GetExerciseList Start... ")
        r= requests.get(self.url + '/numlab/exercises', auth=(self.user, self.pw))
        print(r.status_code)
        print(r.text)
        return True
        
        
    def GetExercise(self, ID):
        print("GetExercise Start...")
        r= requests.get(self.url + '/numlab/exercises/' + str(ID), auth=(self.user, self.pw))
        print(r.status_code)
        print(r.text)
        return True
        
    def PostResults(self):
        print("Post Results Start...")
        with open("../Connector/test_result.json") as json_file:
            json_data = json.load(json_file)
        
        headers = {'Accept' : 'application/json', 'Content-Type' : 'application/json','X-EcsReceiverCommunities':'pinf'}
        r = requests.post(self.url + '/numlab/results',data = json.dumps(json_data),headers = headers, auth=(self.user, self.pw))
        print(r.status_code)
        print (r.text)
        return r.status_code
           

'''
@author: Joshua
'''
import requests
import json

class ConnectTC(object):
    '''
    classdocs
    '''
    url = 'https://nfldevvipecs.rus.uni-stuttgart.de'
    user = ""
    pw = ""
 
    def __init__(self, user, pw):
        self. user = user
        self.pw = pw
        
        '''
        Constructor
        '''
    def PostExercise(self):
        print("Start Post Exercise ...")
        with open("../Connector/test_exercise.json") as json_file:
            json_data = json.load(json_file)
        
        headers = {'Content-Type' : 'application/json','X-EcsReceiverCommunities':'pinf'}
        r = requests.post(self.url + '/numlab/exercises' ,json = str(json_data),headers = headers, auth=(self.user, self.pw))
        print(r.status_code)
       
        return r.status_code
    def GetExercise(self, ID):
        r= requests.get(self.url + '/numlab/exercises/' + str(ID), auth=(self.user, self.pw))
        print(r.status_code)
        return True
    def DelExercise(self, ID):
        r = requests.delete(self.url + '/numlab/exercises/' + str(ID), auth=(self.user, self.pw))
        print(r.status_code)
        return True
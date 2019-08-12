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
        
        headers = {'Content-Type' : 'application/json'}
        r = requests.post(self.url + '/numlab/exercises',data = json.dumps(json_data),headers = headers, auth=(self.user, self.pw))
        print(r.status_code)
        return r.status_code

    def GetExercise(self, ID):
        if ID == False:
            r= requests.get(self.url + '/numblab/exercises', auth=(self.user, self.pw)) 
            print(r.status_code)
            if r.text != "":
                return r.json()       
        else:
            r= requests.get(self.url + '/numblab/exercises/' + ID, auth=(self.user, self.pw))
            print(r.status_code)
            if r.text != "":
                return r.json()
                return r.json()
    def DelExercise(self, ID):
        r = requests.delete('/numblab/exercises/' + ID, auth=(self.user, self.pw))
        print(r.status_code)
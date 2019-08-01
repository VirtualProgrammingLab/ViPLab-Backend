'''
Created on 01.08.2019

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
        r = requests.post(self.url + '/numlab/solutions/fifo', auth=(self.user, self.pw))
        print(r.status_code)
        if r.text != "":
            return r.json()
        
    def GetExerciseList(self):
        r= requests.get(self.url + '/numblab/exercises', auth=(self.user, self.pw)) 
        print(r.status_code)
        if r.text != "":
            return r.json() 
        
        
    def GetExercise(self, ID):
        r= requests.get(self.url + '/numblab/exercises/' + ID, auth=(self.user, self.pw))
        print(r.status_code)
        if r.text != "":
             return r.json()
        
    def PostResults(self, ID):
        payload = ""   ''' Json Data Here '''
        headers = {'content-type': 'application/json'}
        r = requests.post(self.url + '/numlab/results',data = json.dumps(payload), headers = headers, auth=(self.user, self.pw))
        print(r.status_code)
        return r.status_code
           

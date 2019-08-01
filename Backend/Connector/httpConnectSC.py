'''
Created on 01.08.2019

@author: Joshua
'''
import json
import requests
class ConnectSC(object):
    '''
    classdocs
    '''
    url = 'https://nfldevvipecs.rus.uni-stuttgart.de'
    user = ""
    pw = ""
    def __init__(self, user,pw):
        '''
        Constructor
        '''
        self.user = user
        self.pw = pw
    def PostSolution(self):
        payload = ""   ''' Json Data Here '''
        headers = {'content-type': 'application/json'}
        r = requests.post(self.url + '/numlab/solutions',data = json.dumps(payload), headers = headers, auth=(self.user, self.pw))
        return r.status_code
    
    def GetResult(self):
        r = requests.post(self.url + 'numlab/results/fifo', auth = (self.user, self.pw))
        if r.text != "":
            return r.json()
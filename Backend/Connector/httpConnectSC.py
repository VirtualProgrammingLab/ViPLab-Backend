'''
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
        print("Start PostSolution ...")
        payload = json.load(open("../Connector/test_solution.json"))
        headers = {'Content-Type': 'application/json','X-EcsReceiverCommunities':'pinf'}
        r = requests.post(self.url + '/numlab/solutions',data = json.dumps(payload), headers = headers, auth=(self.user, self.pw))
        print (r.status_code)
        print(r.text)
        return True
    
    def GetResult(self):
        print("Start GetResult ...")
        r = requests.post(self.url + '/numlab/results/fifo', auth = (self.user, self.pw))
        print (r.status_code)
        print(r.text)
        return True
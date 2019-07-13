'''
Created on 05.07.2019

@author: Joshua
'''
import requests
import json

def PullCC ():
    request = requests.post(_url('/numlab/solutions'))
    HTMLFile = open('kek.html',"w",encoding = 'utf-8')
    HTMLFile.write(request.text)
    HTMLFile.close()

def PushCC():
    data = Load Json data
    headers = {'Content-type':'application/json','Accept':'text-plain'}
    request = requests.post(_url('/numlab/results'),data=json.dump(data),headers=headers)  
    request
def _url(path):
    return 'https://ecs.uni-stuttgart.de/numlab/' + path

def main():
    PullCC()
   
if __name__== "__main__":
  main()

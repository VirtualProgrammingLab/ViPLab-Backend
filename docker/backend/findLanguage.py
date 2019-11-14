# -*- coding: utf-8 -*-
import threading
import time
import json
import requests
import sys
import docker

running_container = {}
client = docker.from_env()
url = 'https://nfldevvipecs.rus.uni-stuttgart.de'
exercisesQueue = '/numlab/solutions/fifo'


def findLanguage(data):
    lang = list(data["Exercise"]["config"].keys())[0]
    if lang in ["C", "C++"]:
        pass
    elif lang == "Matlab":
        pass
    elif lang == "Octave":
        pass
    elif lang == "Java":
        pass
    elif lang == "DuMuX":
        pass
    elif lang == "Python":
        pass
    else:
        print("No supported lang detected")
    return lang

def createNewContainer(data):
    global running_container
    ''' Sendet einen Post Request an localhost:500/newcontainer, welches einen Kata-Container hochzieht, die Daten an den Container sendet und diesen compilieren lässt '''
    request = requests.post('http://localhost:5001/newcontainer', data=json.dumps(data), headers = {'Content-type': 'application/json'})
    #print(request.json())
    running_container.update(request.json())
    print(running_container)

def returnExitedContainer():
    global running_container
    failedContainer=(client.containers.list(all=True,filters={"exited":1}))
    for all in failedContainer:
        if all.id in running_container:
            print(all.id)
            receiver = running_container[all.id]
            #post zum receiver, dass irgendetwas fehlgeschlagen ist


def getExerciseFromExerciseUrl(exercise_url):
    request = requests.get(exercise_url, auth=("pinfcc2", "YqYsyjVLomICGTY7SK6e"), headers = {'Accept': 'application/json', 'Content-Type': 'application/json'})
    return request.json()

def getSolutionsFromQueue():
    r = requests.get(url + exercisesQueue, auth=("pinfcc2", "YqYsyjVLomICGTY7SK6e"))
    if r.headers.get("Content-Length") == "0":
        print("no new Solution available")
        return None, None, None
    else:
        x_ecsSender = r.headers.get("X-EcsSender")
        exercise_url = r.json().get("Solution").get("exercise")
        return r.json(), x_ecsSender, getExerciseFromExerciseUrl(exercise_url)
    
    
def do_something(solution, receiver, exercise, arg):
    data =  {"Exercise" : exercise.get("Exercise"), "Solution" : solution.get("Solution")}
    lang = findLanguage(data)
    if len(arg)== 1:
        debug = True
    else:
        debug = False
    whole_data = {"data": data, "receiver" : receiver, "debug": debug, "language":lang}
    createNewContainer(whole_data)
    returnExitedContainer()


if __name__ == "__main__":
    arg = sys.argv
    #while(True):
    for _ in range(2):
        solution, receiver, exercise = getSolutionsFromQueue()
        if solution != None:
            t = threading.Thread(target=do_something, args=[solution, receiver, exercise, arg])
            t.start()
            #do_something(solution, receiver, exercise, arg)
        else:
            time.sleep(1.0)
    
    

    
    
    
    '''starttime=time.time()
    i = 1
    while True:
        solution, receiver, exercise = getSolutionsFromQueue()
        if solution != None:
            data = {"Exercise" : exercise.get("Exercise"), "Solution" : solution.get("Solution"), "Receiver" : receiver}
            print(data)
        print("tick" + str(i))
        i += 1
        time.sleep(1.0 - ((time.time() - starttime) % 1.0))'''

# -*- coding: utf-8 -*-
'''
@author Julia
Script to trigger the flask server.
When the ECS can push new solutions from the student, then this script will not be needed anymore -> just trigger the /newcontainer endpoint of the backend
'''
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
    '''
    finds the language the exercise has
    Params:
    - data (dict): '{"Exercise": exercise, "Solution": solution}'
    Return:
    - language the exercise has
    '''
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
    ''' 
    sending a POST request to the flask backend, and triggers the /newcontainer endpoint
    Params:
    - data (dict): '{"data": data, "receiver": receiver, "debug": debug, "language": lang}'
    '''
    
    global running_container
    try:
        request = requests.post('http://localhost:5001/newcontainer', data=json.dumps(data), headers = {'Content-type': 'application/json'})
        running_container.update(request.json())
        return request.status_code

    except:
        return 404



def returnExitedContainer():
    '''
    checks if a container exited with status code 1 -> failed, looks up the student and POST a message to the ECS that something failed
    '''
    
    global running_container
    failedContainer=(client.containers.list(all=True,filters={"exited":1}))
    #print(running_container)
    for all in failedContainer:
        #print(all.id)
        if all.id in running_container:
            print(all.id)
            receiver = running_container[all.id]
            del running_container[all.id]
            #post zum receiver, dass irgendetwas fehlgeschlagen ist


def getExerciseFromExerciseUrl(exercise_url):
    '''
    gets the Exercise from the exercise url
    Params:
    - exercise_url: from a solution
    Return:
    - exercise
    '''
    try:
        request = requests.get(exercise_url, auth=("pinfcc2", "YqYsyjVLomICGTY7SK6e"), headers = {'Accept': 'application/json', 'Content-Type': 'application/json'})
        return request.json()
    except:
        return 404

def getSolutionsFromQueue():
    '''
    checks if a new solution is in the solutions/fifo. -> Production System: change GET-Method to POST-Method
    Return:
    - None, None, None: if content-length = 0, means: "no new solution is in the solutions/fifo"
    - solution, x_ecsSender, [getExerciseFromExerciseUrl(exercise_url) -> exercise from exercise url]
    '''
    
    r = requests.post(url + exercisesQueue, auth=("pinfcc2", "YqYsyjVLomICGTY7SK6e"))
    if r.headers.get("Content-Length") == "0":
        print("no new Solution available")
        return None, None, None
    else:
        x_ecsSender = r.headers.get("X-EcsSender")
        #try:
        exercise_url = r.json().get("Solution").get("exercise")
        return r.json(), x_ecsSender, getExerciseFromExerciseUrl(exercise_url)
        #except:
        #    return None, None, None
    
    
def do_something(solution, receiver, exercise, arg):
    '''
    starts the needed Workflow
    Params:
    - solution (dict)
    - receiver 
    - exercise
    - arg (bool): debug param -> True, if container will be removed after compiling, False, if container will not be removed -> if an argument was passed while starting the script -> Debug=True, else Debug=False
    '''
    data =  {"Exercise" : exercise.get("Exercise"), "Solution" : solution.get("Solution")}
    lang = findLanguage(data)
    if len(arg)== 1:
        debug = True
    else:
        debug = False
    whole_data = {"data": data, "receiver" : receiver, "debug": debug, "language":lang}
    statuscode = createNewContainer(whole_data)
    if statuscode != 201:
        createNewContainer(whole_data)
    returnExitedContainer()
    print(statuscode)


if __name__ == "__main__":
    '''
    main method: starts for each solution from the solution queue a new thread, else if no new solution is in solutions/fifo, it waits 1 sec. and starts a new try
    '''
    starttime = time.time()
    arg = sys.argv #from starting this script
    while(True): 
        solution, receiver, exercise = getSolutionsFromQueue()
        if solution != None:
            t = threading.Thread(target=do_something, args=[solution, receiver, exercise, arg])                
            t.start()
            #do_something(solution, receiver, exercise, arg)
            #t.join()
            #print(time.time()-starttime)
        else:
            d=True
            time.sleep(1.0)
        t.join()
        #print(time.time()-starttime)
    t.join()
    print(time.time()-starttime)
    

    
    
    
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

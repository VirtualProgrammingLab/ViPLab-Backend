# -*- coding: utf-8 -*-

import json 
import requests

def printResult(result):
    print("Result ist: ")
    print(result)

def readJson(input):
    with open(input, "r") as f:
        return json.load(f)

pathToExercise = "./examples/exercise.json" # replace 'None' with path to exercise
pathToSolution = "./examples/solution.json" # replace 'None' with path to solution

def findLanguage(pathToExercise, pathToSolution):
    '''
    Findet über den Pfad in Solution die Exercise und damit die Programmiersprache der Aufgabe
    '''
    data = {"Exercise": readJson(pathToExercise)["Exercise"], "Solution": readJson(pathToSolution)["Solution"]}
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
    return lang, data

def createNewContainer(lang, data):
    ''' Sendet einen Post Request an localhost:500/newcontainer, welches einen Kata-Container hochzieht, 
    die Daten an den Container sendet und diesen compilieren lässt '''
    data=json.dumps({"language":lang, "data":data, "receiver":"receiver"})
    request = requests.post('http://localhost:5001/newcontainer', data=data, headers = {'Content-type': 'application/json'})
    print(request.text)
    

if __name__ == "__main__":
    lang, data= findLanguage(pathToExercise, pathToSolution)  
    createNewContainer(lang, data)  

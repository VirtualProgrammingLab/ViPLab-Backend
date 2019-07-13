import json

def readJson(input):
    #try to read input data as file name
    try:
        with open(input, "r") as f:
            return json.load(f)
    except Exception:
        pass
    #try to read input data as json string
    try:
        return json.loads(input)
    except Exception:
        pass
    #if nothing found, return None
    return None

class Exercise:
    def __init__(self, data):
        self.postTime = data["Exercise"]["postTime"]
        self.ttl = data["Exercise"]["TTL"]
        self.identifier = data["Exercise"]["identifier"]
        self.department = data["Exercise"]["department"]
        self.comment = data["Exercise"]["comment"]
        self.name = data["Exercise"]["name"]
        self.description = data["Exercise"]["description"]
        self.elements = data["Exercise"]["elements"]
        self.environment = data["Exercise"]["environment"]
        self.config = data["Exercise"]["config"]
        self.lang = self.__getLang()

    def __getLang(self):
        languages = ["C", "C++", "Matlab", "Octave", "Java", "DuMuX", "Python"]
        for lang in languages:
            if lang in self.config:
                return lang
        return None
    
    def getCompilingCommand(self):
        return self.config[self.lang]["compiling"]["compiler"] + " " + \
            self.config[self.lang]["compiling"]["flags"]

class Solution:
    def __init__(self, data):
        self.postTime = data["Solution"]["postTime"]
        self.id = data["Solution"]["ID"]
        self.evaluationService = data["Solution"]["evaluationService"]
        self.comment = data["Solution"]["comment"]
        self.exercise = data["Solution"]["exercise"]
        self.exerciseModifications = data["Solution"]["exerciseModifications"]
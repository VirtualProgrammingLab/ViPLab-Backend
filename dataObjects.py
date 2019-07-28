import json, urllib.request
import datetime as dt

class InvalidJsonData(Exception):
    pass

def readJson(input):
    """ Trying to read JSON from given input.
        Interpreting input as path to json file first,
        then interpreting input as json string.

        If both failed, raise InvalidJsonData Exception
    """
    #try to read input data as path
    try:
        with open(input, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        pass
    #try to read input data as json string
    try:
        return json.loads(input)
    except json.JSONDecodeError:
        pass
    #if nothing found, return None
    raise InvalidJsonData()

class Exercise:
    def __init__(self, data):
        # elements retrieved with .get are optional and
        # return None if not found
        self.postTime = data["Exercise"]["postTime"]
        self.ttl = data["Exercise"].get("TTL")
        self.identifier = data["Exercise"]["identifier"]
        self.department = data["Exercise"].get("department")
        self.comment = data["Exercise"].get("comment")
        self.name = data["Exercise"].get("name")
        self.description = data["Exercise"].get("description")
        self.elements = data["Exercise"]["elements"]
        self.environment = data["Exercise"].get("environment")
        self.routing = data["Exercise"].get("routing")
        self.elementMap = data["Exercise"].get("elementMap")
        self.elementProperties = data["Exercise"].get("elementProperties")
        self.config = data["Exercise"].get("config")
        # adding language of Exercise
        self.lang = self.__getLang()

    def createJson(self):
        """ creating a JSON string from exercise object """
        # all data stored in the exercise object
        data = {
            "postTime" : self.postTime,
            "ttl" : self.ttl,
            "identifier" : self.identifier,
            "department" : self.department,
            "comment" : self.comment,
            "name" : self.name,
            "description" : self.description,
            "elements" : self.elements,
            "environment" : self.environment,
            "routing" : self.routing,
            "elementMap" : self.elementMap,
            "elementProperties" : self.elementProperties,
            "config" : self.config
        }
        # remove all "None" data
        for d in data:
            if d is None:
                data.pop(d, None)
        return json.dumps(data, indent=4)
    
    def getCompilingCommand(self):
        """ retrieving compiling command """
        return self.config[self.lang]["compiling"]["compiler"] + " " + \
            self.config[self.lang]["compiling"]["flags"]

    def __getLang(self):
        """ retrieving language of exercise """
        languages = ["C", "C++", "Matlab", "Octave", "Java", "DuMuX", "Python"]
        for lang in languages:
            if lang in self.config:
                return lang
        return None

class Solution:
    def __init__(self, data, exercise = None):
        self.postTime = data["Solution"]["postTime"]
        self.id = data["Solution"]["ID"]
        self.evaluationService = data["Solution"].get("evaluationService")
        self.comment = data["Solution"].get("comment")
        self.exerciseUrl = data["Solution"]["exercise"]
        self.exerciseModifications = data["Solution"].get("exerciseModifications")
        self.exercise = self.getExercise() if exercise == None else exercise

    def getExercise(self):
        """ retrieving exercise json and create exercise object """
        with urllib.request.urlopen(self.exerciseUrl) as url:
            data = json.loads(url.read().decode())
            return Exercise(data)

    def createJson(self):
        """ creating a JSON string from solution object """
        data = {
            "postTime" : self.postTime,
            "ID" : self.id,
            "evaluationService" : self.evaluationService,
            "comment" : self.comment,
            "exercise" : self.exerciseUrl,
            "exerciseModifications" : self.exerciseModifications
        }
        for d in data:
            if d is None:
                data.pop(d, None)
        return json.dumps(data, indent=4)
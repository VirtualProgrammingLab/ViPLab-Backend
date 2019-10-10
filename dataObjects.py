import json, urllib.request
from datetime import datetime as dt

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
        """ Constructor for exercise object.
        
        Args:
            data: exercise data parsed by readJson
        """
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
        """ Creates a JSON out of the exercise object 
        
        Returns:
            A string containing the JSON data
        """
        #struct with all possible data
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
        #removes optional entries if no value is given
        for d in data:
            if d is None:
                data.pop(d, None)
        return json.dumps(data, indent=4)
    
    def getCompilingCommand(self):
        """ retrieving compiling command """
        return self.config[self.lang]["compiling"]["compiler"] + " " + \
            self.config[self.lang]["compiling"]["flags"]

    def __getLang(self):
        """ Retrieving language of exercise

        Returns:
            The programming language of the exercise, given in config
        """
        languages = ["C", "C++", "Matlab", "Octave", "Java", "DuMuX", "Python"]
        for lang in languages:
            if lang in self.config:
                return lang
        return None

class Solution:
    """ Solution object
    
    Documentation:
        https://campusconnect.tik.uni-stuttgart.de/HeikoBernloehr/FreeLancer/ECS/ecs2/NumLab/solutions
    """
    def __init__(self, data, exercise : Exercise = None):
        """ Constructor for solution object.
        
        Args:
            data (str): solution data parsed by readJson
            exercise (Exercise): optional exercise object. If not given, it will
                try to retrieve it from exercise url
        """
        self.postTime = data["Solution"]["postTime"]
        self.id = data["Solution"]["ID"]
        self.evaluationService = data["Solution"].get("evaluationService")
        self.comment = data["Solution"].get("comment")
        self.exerciseUrl = data["Solution"]["exercise"]
        self.exerciseModifications = data["Solution"].get("exerciseModifications")
        self.exercise = self.getExercise() if exercise == None else exercise

    def getExercise(self):
        """ Retrieves the given exercise json and creates exercise object
        """
        with urllib.request.urlopen(self.exerciseUrl) as url:
            data = json.loads(url.read().decode())
            return Exercise(data)

    def createJson(self):
        """ Creates a JSON out of the solution object 
        
        Returns:
            A string containing the JSON data
        """
        #struct with all possible data
        data = {
            "postTime" : self.postTime,
            "ID" : self.id,
            "evaluationService" : self.evaluationService,
            "comment" : self.comment,
            "exercise" : self.exerciseUrl,
            "exerciseModifications" : self.exerciseModifications
        }
        #removes optional entries if no value is given
        for d in data:
            if d is None:
                data.pop(d, None)
        
        return json.dumps(data, indent=4)

class Result:
    """ Result object
    
    Documentation:
        https://campusconnect.tik.uni-stuttgart.de/HeikoBernloehr/FreeLancer/ECS/ecs2/NumLab/results
    """
    def __init__(self, solution : str, comment : str = None, 
                 status : str = "final"):
        """ Constructor for result object.
        
        Args:
            solution (str): JSON string containing the solution data
            comment (str): optional comment
            status (str): has to be "final" or "intermediate"
        """
        self.time = dt.now()
        self.solution = solution
        self.id = dt.strftime(dt.now(), "%Y-%m-%d %H:%M:%S")
        self.comment = comment
        self.status = status
        self.index = 0
        self.computation = {
            "startTime" : dt.strftime(self.time, "%Y-%m-%d %H:%M:%S")
        }
        self.elements = []

    def calculateComputationTime(self):
        """ Adds finish time and time delta to computation dict
        """
        time = dt.now()
        self.computation["finishTime"] = dt.strftime(time, "%Y-%m-%d %H:%M:%S")
        self.computation["duration"] = time - self.time()

    def addComputationInfos(self, ccVersionLong : str, ccVersion : str,
            chainVersion : str, technicalInfo : dict, userInfo : dict):
        """ Adds required informations about the CC 

        Args:
            ccVersionLong (str):
            ccVersion (str):
            chainVersion (str):
            technicalInfo (dict):
            userInfo (dict):
        """
        self.computation["CC_versionLong"] = ccVersionLong
        self.computation["CC_version"] = ccVersion,
        self.computation["chain_version"] = chainVersion
        self.computation["technicalInfo"] = technicalInfo
        self.computation["userInfo"] = userInfo

    def createJson(self):
        """ Creates a JSON out of the result object 
        
        Returns:
            A string containing the JSON data
        """
        #struct with all possible data
        data = {
            "Result" : {
                "ID" : self.id,
                "comment" : self.comment,
                "status" : self.status,
                "index" : self.index,
                "computation" : self.computation,
                "Solution" : self.solution,
                "elements" : self.elements
            }
        }
        #removes optional entries if no value is given
        if data.get("comment") is None:
            data.pop("comment", None)
        if data.get("index") is None:
            data.pop("index", None)
        
        return json.dumps(data, indent=4)
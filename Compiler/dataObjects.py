import json, requests, os, socket
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
    except:
        pass
    #try to read input data as json string
    try:
        return json.loads(input)
    except:
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
        tmp = data["Exercise"].get("config")
        if tmp is not None:
            self.lang = list(tmp.keys())[0]
            self.config = tmp[self.lang]
            # adding language of Exercise

    def createJson(self):
        """ Creates a JSON out of the exercise object 
        
        Returns:
            A string containing the JSON data
        """
        #struct with all possible data
        data = {
            "Exercise" : {
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
        }
        #removes optional entries if no value is given
        for d in data["Exercise"]:
            if d is None:
                data["Exercise"].pop(d, None)

        return json.dumps(data, indent=4)
    
    def getCompilingCommand(self):
        """ retrieving compiling command """
        compiler = self.config["compiling"]["compiler"]
        if compiler is None or compiler == "":
            compiler = "gcc" if self.lang == "C" else "g++"
        return f"{compiler} {self.config['compiling']['flags']}"

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
        r = requests.get(self.exerciseUrl)
        return Exercise(r.json())

    def createJson(self):
        """ Creates a JSON out of the solution object 
        
        Returns:
            A string containing the JSON data
        """
        #struct with all possible data
        data = {
            "Solution" : {
                "postTime" : self.postTime,
                "ID" : self.id,
                "evaluationService" : self.evaluationService,
                "comment" : self.comment,
                "exercise" : self.exerciseUrl,
                "exerciseModifications" : self.exerciseModifications
            }
        }
        #removes optional entries if no value is given
        for d in data["Solution"]:
            if d is None:
                data["Solution"].pop(d, None)
        
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
        self.id = dt.strftime(self.time, "%Y-%m-%d %H:%M:%S")
        self.comment = comment
        self.status = status
        self.index = None
        self.computation = {
            "startTime" : dt.strftime(self.time, "%Y-%m-%d %H:%M:%S"),
            "CC_versionLong" : "",
            "CC_version" : "",
            "chain_version" : "",
            "technicalInfo" : {
                "host" : socket.gethostname(),
                "PID" : os.getpid(),
                "ID" : "#1"
            },
            "userInfo" : {}
        }
        self.elements = []

    def setId(self, id: int):
        self.computation["technicalInfo"]["ID"] = f"#{id}"

    def calculateComputationTime(self):
        """ Adds finish time and time delta to computation dict
        """
        time = dt.now()
        self.computation["finishTime"] = dt.strftime(time, "%Y-%m-%d %H:%M:%S")
        self.computation["duration"] = time - self.time

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
        if data["Result"].get("comment") is None:
            data["Result"].pop("comment", None)
        if data["Result"].get("index") is None:
            data["Result"].pop("index", None)
        
        return json.dumps(data, indent=2, default=str)
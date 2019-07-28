import os, subprocess
from enum import Enum

class CState(Enum):
    MERGING = 0
    COMPILING = 1
    CHECKING = 2
    LINKING = 3
    RUNNING = 4
    
path = "temp"

class Compiler:     
    def __del__(self):
        if os.path.isdir(path):
            for f in os.scandir(path):
                os.remove(f.path)
            print("temp folder cleared")

class C(Compiler):
    def __init__(self, solution):
        path = os.getcwd()
        self.solution = solution
        self.lang = self.solution.exercise.lang
        maxState = CState[self.getMaxState()]
        self.merge()
        if CState.COMPILING.value <= maxState.value:
            self.compile()
        if CState.CHECKING.value <= maxState.value and self.lang == "C":
            self.check()
        if CState.LINKING.value <= maxState.value:
            self.link()
        if CState.RUNNING.value <= maxState.value:
            self.run()
        os.chdir(path)

    def getMaxState(self):
        s = self.solution.exercise.config[self.lang].get("stopAfterPhase")
        return s.upper() if s is not None else "RUNNING"

    def merge(self):
        """ retrieving code from exercise and solution objects
            and writing it to file """
        # replacing exercise code with student solution
        for sEl in self.solution.exerciseModifications["elements"]:
            for eEl in self.solution.exercise.elements:
                if eEl["identifier"] == sEl["identifier"] and eEl["modifiable"] == True:
                    eEl["value"] = sEl["value"]
        #concatenating code     
        code = ""
        for e in self.solution.exercise.elements:
            code += e["value"]
            if code[-1] != "\n":
                code += "\n"
        #check if temp dir exists
        if not os.path.exists(path):
            os.makedirs(path)
        os.chdir(path)
        with open("temp.c", "w+") as f:
            f.write(code)

    def compile(self):
        com = (self.solution.exercise.getCompilingCommand() + " -o temp temp.c").split(" ")
        result = subprocess.run(com, stdout=subprocess.PIPE)
        print(result.stdout.decode("utf-8"))

    def check(self):
        pass

    def link(self):
        pass
    
    def run(self):
        os.chmod("temp", 0o700)
        com = "./temp".split(" ")
        result = subprocess.run(com, stdout=subprocess.PIPE)
        print(result.stdout.decode("utf-8"))
        
class Matlab(Compiler):
    def __init__(self, solution):
        print("Matlab")

class Octave(Compiler):
    def __init__(self, solution):
        print("Octave")

class Java(Compiler):
    def __init__(self, solution):
        print("Java")

class DuMuX(Compiler):
    def __init__(self, solution):
        print("DuMuX")

class Python(Compiler):
    def __init__(self, solution):
        print("Python")

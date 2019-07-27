import os, subprocess

path = "temp"

class Compiler:     
    def __del__(self):
        if os.path.isdir(path):
            for f in os.scandir(path):
                os.remove(f.path)
            print("Cleared")

class C(Compiler):
    def __init__(self, solution):
        path = os.getcwd()
        self.solution = solution
        self.createFiles()
        self.compileFiles()
        self.runFiles()
        os.chdir(path)
    
    def createFiles(self):
        if not os.path.exists(path):
            os.makedirs(path)
        os.chdir(path)
        print("Write the following code to a file: \n" + self.solution.getCode())
        with open("temp.c", "w+") as f:
            f.write(self.solution.getCode())

    def compileFiles(self):
        print("Compiling files")
        com = (self.solution.exercise.getCompilingCommand() + " -o temp temp.c").split(" ")
        result = subprocess.run(com, stdout=subprocess.PIPE)
        print(result.stdout.decode("utf-8"))
    
    def runFiles(self):
        print("running main. Output:")
        os.chmod("temp", 0o700)
        com = "./temp".split(" ")
        result = subprocess.run(com, stdout=subprocess.PIPE)
        print(result.stdout.decode("utf-8"))
        
class Cpp(Compiler):
    def __init__(self, solution):
        print("C++")

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

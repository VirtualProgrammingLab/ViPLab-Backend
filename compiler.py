import os

class Compiler:
    def clearTempFiles(self):
        if os.path.isdir("temp"):
            for f in os.scandir("temp"):
                os.remove(f.path)
                print("Cleared")
            

class C(Compiler):
    def __init__(self, exercise, solution):
        print("C")

class Cpp(Compiler):
    def __init__(self, exercise, solution):
        print("C++")

class Matlab(Compiler):
    def __init__(self, exercise, solution):
        print("Matlab")

class Octave(Compiler):
    def __init__(self, exercise, solution):
        print("Octave")

class Java(Compiler):
    def __init__(self, exercise, solution):
        print("Java")

class DuMuX(Compiler):
    def __init__(self, exercise, solution):
        print("DuMuX")

class Python(Compiler):
    def __init__(self, exercise, solution):
        print("Python")

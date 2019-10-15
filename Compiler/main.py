import subprocess, dataObjects, sys, os
from Compiler.c import C
from Compiler.dumux import Dumux
from Compiler.java import Java
from Compiler.matlab import Matlab
from Compiler.octave import Octave
from Compiler.python import Python

mainPath = os.path.dirname(os.path.abspath(sys.argv[0]))

#Path to JSON example files
pte = os.path.join(mainPath, "examples", "exercise.json")
pti = os.path.join(mainPath, "examples", "interrupt.json")
ptr = os.path.join(mainPath, "examples", "result.json")
pts = os.path.join(mainPath, "examples", "solution.json")
#generic = os.path.join(mainPath, "examples", "generic.noModifications.solution.json")
#mulSource = os.path.join(mainPath, "examples", "C.compiling.sources_2.ex.json")

if __name__ == "__main__":
    #exercise = dataObjects.Exercise(dataObjects.readJson(mulSource))
    #solution = dataObjects.Solution(dataObjects.readJson(generic), exercise)
    exercise = dataObjects.Exercise(dataObjects.readJson(pte))
    solution = dataObjects.Solution(dataObjects.readJson(pts), exercise)

    comp = None
    if solution.exercise.lang in ["C", "C++"]:
        comp = C(solution)
    elif solution.exercise.lang == "Matlab":
        comp = Matlab(solution)
    elif solution.exercise.lang == "Octave":
        comp = Octave(solution)
    elif solution.exercise.lang == "Java":
        comp = Java(solution)
    elif solution.exercise.lang == "DuMuX":
        comp = Dumux(solution)
    elif solution.exercise.lang == "Python":
        comp = Python(solution)

    if comp is not None:
        comp.processData()
    else:
        print("No supported language detected")
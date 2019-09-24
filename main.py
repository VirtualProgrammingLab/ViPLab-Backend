import subprocess, dataObjects, compiler
from Compiler.c import C
from Compiler.dumux import Dumux
from Compiler.java import Java
from Compiler.matlab import Matlab
from Compiler.octave import Octave
from Compiler.python import Python

#Path to JSON example files
pte = "examples/exercise.json"
pti = "examples/interrupt.json"
ptr = "examples/result.json"
pts = "examples/solution.json"
generic = "examples/generic.noModifications.solution.json"
mulSource = "examples/C.compiling.sources_2.ex.json"

if __name__ == "__main__":
    #exercise = dataObjects.Exercise(dataObjects.readJson(mulSource))
    #solution = dataObjects.Solution(dataObjects.readJson(generic), exercise)
    exercise = dataObjects.Exercise(dataObjects.readJson(pte))
    solution = dataObjects.Solution(dataObjects.readJson(pts), exercise)
    if solution.exercise.lang in ["C", "C++"]:
        C(solution)
    elif solution.exercise.lang == "Matlab":
        Matlab(solution)
    elif solution.exercise.lang == "Octave":
        Octave(solution)
    elif solution.exercise.lang == "Java":
        Java(solution)
    elif solution.exercise.lang == "DuMuX":
        Dumux(solution)
    elif solution.exercise.lang == "Python":
        Python(solution)
    else:
        print("No supported lang detected")
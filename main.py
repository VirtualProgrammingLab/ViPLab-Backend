from parseExercise import parseExercise
import subprocess, dataObjects, compiler

#Path to JSON example files
pte = "examples/exercise.json"
pti = "examples/interrupt.json"
ptr = "examples/result.json"
pts = "examples/solution.json"

if __name__ == "__main__":
    exercise = dataObjects.Exercise(dataObjects.readJson(pte))
    solution = dataObjects.Solution(dataObjects.readJson(pts))
    l = exercise.lang
    comp = None
    if l == "C":
        comp = compiler.C(exercise, solution)
    elif l == "C++":
        comp = compiler.Cpp(exercise, solution)
    elif l == "Matlab":
        comp = compiler.Matlab(exercise, solution)
    elif l == "Octave":
        comp = compiler.Octave(exercise, solution)
    elif l == "Java":
        comp = compiler.Java(exercise, solution)
    elif l == "DuMuX":
        comp = compiler.DuMuX(exercise, solution)
    elif l == "Python":
        comp = compiler.Python(exercise, solution)
    else:
        print("No supported lang detected")

    comp.clearTempFiles()
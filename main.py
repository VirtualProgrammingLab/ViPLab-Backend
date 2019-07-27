from parseExercise import parseExercise
import subprocess, dataObjects, compiler

#Path to JSON example files
pte = "examples/exercise.json"
pti = "examples/interrupt.json"
ptr = "examples/result.json"
pts = "examples/solution.json"

if __name__ == "__main__":
    exercise = dataObjects.Exercise(dataObjects.readJson(pte))
    solution = dataObjects.Solution(dataObjects.readJson(pts), exercise)
    if solution.exercise.lang == "C":
        compiler.C(solution)
    elif solution.exercise.lang == "C++":
        compiler.Cpp(solution)
    elif solution.exercise.lang == "Matlab":
        compiler.Matlab(solution)
    elif solution.exercise.lang == "Octave":
        compiler.Octave(solution)
    elif solution.exercise.lang == "Java":
        compiler.Java(solution)
    elif solution.exercise.lang == "DuMuX":
        compiler.DuMuX(solution)
    elif solution.exercise.lang == "Python":
        compiler.Python(solution)
    else:
        print("No supported lang detected")
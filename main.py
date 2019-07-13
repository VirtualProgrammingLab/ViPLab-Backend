from parseExercise import parseExercise
import subprocess, os

#Path to JSON example files
pte = "examples/exercise.json"
pti = "examples/interrupt.json"
ptr = "examples/result.json"
pts = "examples/solution.json"

def parseJson(exercise, solution):
    lang, compileExec, code = parseExercise(exercise, solution)
    if lang == "C":
        execC(compileExec, code)
    elif lang == "C++":
        execCpp(compileExec, code)
    elif lang == "Matlab":
        execMatlab(compileExec, code)
    elif lang == "Octave":
        execOctave(compileExec, code)
    elif lang == "Java":
        execJava(compileExec, code)
    elif lang == "DuMuX":
        execDuMuX(compileExec, code)
    elif lang == "Python":
        execPython(compileExec, code)
    else:
        print("No supported lang detected")

def execC(exec, code):
    with open("temp.c", "w+") as f:
            f.write(code)
    exec += ["temp.c", "-o", "temp.out"]
    print("Compile command:\n" + " ".join(exec))
    try:
        print("Compiling!")
        comp = subprocess.run(exec, stdout=subprocess.PIPE)
        print("Output:\n" + comp.stdout.decode('utf-8'))

        print("\nMaking compiled file executable")
        out = subprocess.run(["chmod", "+x", "temp.out"], stdout=subprocess.PIPE)
        print("Output:\n" + out.stdout.decode('utf-8'))

        print("\nRunning compiled file")
        out = subprocess.run(["./temp.out"], stdout=subprocess.PIPE)
        print("Output:\n" + out.stdout.decode('utf-8'))
    except FileNotFoundError:
        print("gcc not found, skipped compiling")
        
    print("\nRemoving temp files")
    try:
        os.remove("temp.c")
    except FileNotFoundError:
        pass

    try:
        os.remove("temp.out")
    except FileNotFoundError:
        pass

def execCpp(exec, code):
    pass

def execCpp(exec, code):
    pass
def execMatlab(exec, code):
    pass
def execOctave(exec, code):
    pass
def execJava(exec, code):
    pass
def execDuMuX(exec, code):
    pass
def execPython(exec, code):
    pass

def clearTempFiles():
    for f in os.scandir("temp"):
        os.remove(f.path)

if __name__ == "__main__":
    parseJson(pte, pts)
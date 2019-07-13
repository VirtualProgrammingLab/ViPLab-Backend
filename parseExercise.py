import json

def parseExercise(exercise, solution):
    #reading given json, given as string or as path to file
    eData = __readJson(exercise)
    sData = __readJson(solution)
    if eData is None or sData is None:
        print("No data found")
        return

    lang = __getLang(eData["Exercise"]["config"])
    code = __concatenateExercise(
                eData["Exercise"]["elements"], 
                sData["Solution"]["exerciseModifications"]["elements"]
            )
    compileExec = __getCompiler(eData["Exercise"]["config"][lang]["compiling"])
    return lang, compileExec, code

def __readJson(input):
    #try to read input data as file name
    try:
        with open(input, "r") as f:
            return json.load(f)
    except Exception:
        pass
    #try to read input data as json string
    try:
        return json.loads(input)
    except Exception:
        pass
    #if nothing found, return None
    return None

def __getCompiler(comp):
        l = []
        l.append(comp["compiler"])
        flags = comp["flags"].split(" ")
        for f in flags:
            l.append(f)
        return l

def __concatenateExercise(eElements, sElements):
    #replacing exercise code with students solution
    for se in sElements:
        s = se["identifier"]
        for ee in eElements:
            if ee["identifier"] == s and ee["modifiable"] == True:
                ee["value"] = se["value"]
    #concatenating code segments
    code = ""
    #check if all segments but the last ends with "\n". If not, adds it
    for e in eElements[:-1]:
        code += e["value"] + "\n" if e["value"][-1] != "\n" else code + e["value"]
    return code + eElements[len(eElements) -1]["value"]
    
def __getLang(conf):
    languages = ["C", "C++", "Matlab", "Octave", "Java", "DuMuX", "Python"]
    for lang in languages:
        if lang in conf:
            return lang
    return None
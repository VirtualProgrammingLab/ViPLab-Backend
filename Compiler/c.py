import os, subprocess

PATH = "temp"
DEBUG = False

class C:
    def __del__(self):
        if os.path.isdir(PATH) and not DEBUG:
            for f in os.scandir(PATH):
                os.remove(f.path)
            print("temp folder cleared")

    def __init__(self, solution):
        print("Language: C/C++\n---")
        if not os.path.exists(PATH):
            os.makedirs(PATH)
            print("created temp folder")
        curpath = os.getcwd()
        self.solution = solution
        self.lang = self.solution.exercise.lang
        maxState = self.getMaxState()
        self.replaceCodeWithSolution()
        self.fileext = ".c" if self.lang == "C" else ".cpp"
        filenames = self.merge()
        if 1 <= maxState:
            self.compile(filenames)
        if 2 <= maxState and self.lang == "C":
            self.check()
        if 3 <= maxState:
            self.link(filenames)
        if 4 <= maxState:
            self.run()
        os.chdir(curpath)

    def getMaxState(self) -> int:
        s = self.solution.exercise.config[self.lang].get("stopAfterPhase")
        return 4 if s is None or s == "running" else \
            3 if s == "linking" else \
            2 if s == "checking" else \
            1 if s == "compiling" else 0
    
    def replaceCodeWithSolution(self):
        # replacing exercise code with student solution
        for sEl in self.solution.exerciseModifications["elements"]:
            for eEl in self.solution.exercise.elements:
                if eEl["identifier"] == sEl["identifier"] and eEl["modifiable"] == True:
                    eEl["value"] = sEl["value"]

    def merge(self):
        print("Merging\n---")
        os.chdir(PATH)
        if len(self.solution.exercise.config[self.lang]["merging"]) == 1:
            return self.mergeSingleFile()
        else:
            return self.mergeMultipleFiles()

    def mergeSingleFile(self) -> list:
        code = ""
        for s in self.solution.exercise.config[self.lang]["merging"]["sources"]:
            for e in self.solution.exercise.elements:
                if s == e["identifier"]:
                    code += e["value"]
                    if code[-1] != "\n":
                        code += "\n"
                    break

        with open("temp" + self.fileext, "w+") as f:
            f.write(code)
        return ["temp"]

    def mergeMultipleFiles(self) -> list:
        l = []
        for m in self.solution.exercise.config[self.lang]["merging"]:
            code = ""
            for s in m["sources"]:
                for e in self.solution.exercise.elements:
                    if s == e["identifier"]:
                        code += e["value"]
                        if code[-1] != "\n":
                            code += "\n"
                        break
                
            fname = m["mergeID"] 
            with open(fname + self.fileext, "w+") as f:
                f.write(code)
            l.append(fname)
        return l

    def compile(self, filenames):
        print("Compiling")
        files = self.solution.exercise.config[self.lang]["compiling"].get("sources")
        files = files if files is not None else filenames
        com = self.solution.exercise.getCompilingCommand() + " -c "
        com += " ".join([s + self.fileext for s in files])
        print("Compiling command: " + com)
        result = subprocess.run(com.split(" "), stdout=subprocess.PIPE)
        print("Compiling Output:\n" + result.stdout.decode("utf-8"))
        print("---")

    def check(self):
        print("Checking - WIP")
        code = ""
        sources = self.solution.exercise.config[self.lang].get("checking")
        if sources is not None:
            sources = sources["sources"]
            for s in sources:
                for e in self.solution.exercise.elements:
                    if s == e["identifier"]:
                        code = e["value"]
                        # Todo: check for illegal system calls in code
                        break
        print("---")

    def link(self, files):
        print("Linking")
        flags = self.solution.exercise.config[self.lang]["linking"]["flags"]
        com = "gcc" if self.lang == "C" else "g++"
        com += " -o out " + " ".join([s + ".o" for s in files]) + " " + flags
        print("Linking command: " + com)
        result = subprocess.run(com.split(" "), stdout=subprocess.PIPE)
        print("Linking Output:\n" + result.stdout.decode("utf-8"))
        print("---")
    
    def run(self):
        print("Running")
        os.chmod("out", 0o700)
        com = "./out"
        print("Running command: " + com)
        result = subprocess.run(com.split(" "), stdout=subprocess.PIPE)
        print("Running Output:\n" + result.stdout.decode("utf-8"))
        print("---")
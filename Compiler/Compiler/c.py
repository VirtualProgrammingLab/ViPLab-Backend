import os, sys, subprocess, dataObjects
from pycparser import c_parser, c_ast, parse_file

PATH = os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])), "temp")
DEBUG = True

class C:
    def __del__(self):
        if os.path.isdir(PATH) and not DEBUG:
            for f in os.scandir(PATH):
                os.remove(f.path)
            print("temp folder cleared")

    def __init__(self, solution : dataObjects.Solution):
        self.result = dataObjects.Result(solution.createJson())
        print("Language: C/C++\n---")
        if not os.path.exists(PATH):
            os.makedirs(PATH)
            print("created temp folder")
        curpath = os.getcwd()
        self.solution = solution
        self.lang = self.solution.exercise.lang
        maxState = self.getMaxState()
        maxState = 2
        self.replaceCodeWithSolution()
        self.fileext = ".c" if self.lang == "C" else ".cpp"
        fileInfo = self.merge()
        if 1 <= maxState:
            self.compile(fileInfo)
        if 2 <= maxState and self.lang == "C":
            self.check(fileInfo)
        if 3 <= maxState:
            self.link(fileInfo)
        if 4 <= maxState:
            self.run()
        self.result.calculateComputationTime()
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
        print("Merging")
        os.chdir(PATH)
        if len(self.solution.exercise.config[self.lang]["merging"]) == 1:
            return self.mergeSingleFile()
        else:
            return self.mergeMultipleFiles()
        print("---")

    def mergeSingleFile(self) -> dict:
        r = {"temp" : {}}
        code = ""
        loc = 0
        for s in self.solution.exercise.config[self.lang]["merging"]["sources"]:
            for e in self.solution.exercise.elements:
                if s == e["identifier"]:
                    r["temp"][s] = (loc + 1)
                    code += e["value"]
                    if not code.endswith("\n"):
                        code += "\n"
                    loc += e["value"].count("\n")
                    break
        loc += 1
        with open(f"temp.{self.fileext}", "w+") as f:
            f.write(code)
        print(r)
        return r

    def mergeMultipleFiles(self) -> dict:
        r = {}
        for m in self.solution.exercise.config[self.lang]["merging"]:
            fname = m["mergeID"] 
            loc = 0
            r[fname] = {}
            code = ""
            for s in m["sources"]:
                for e in self.solution.exercise.elements:
                    if s == e["identifier"]:
                        r[fname][s] = (loc + 1)
                        code += e["value"]
                        if not code.endswith("\n"):
                            code += "\n"
                    loc += e["value"].count("\n")
                    break
            loc += 1
            with open(f"{fname}.{self.fileext}", "w+") as f:
                f.write(code)
        print(r)
        return r

    def compile(self, fileInfo):
        print("Compiling")
        files = self.solution.exercise.config[self.lang]["compiling"].get("sources")
        files = files if files is not None else fileInfo
        com = self.solution.exercise.getCompilingCommand() + " -c "
        com += " ".join([s + self.fileext for s in files])
        print("Compiling command: " + com)
        result = subprocess.run(com.split(" "), stdout=subprocess.PIPE)
        print("Compiling Output:\n" + result.stdout.decode("utf-8"))
        print("---")

    def check(self, fileInfo):
        print("Checking - WIP")
        checker = Checker(fileInfo)
        for a in checker.asts:
            checker.show_func_defs(checker.asts[a])
        print("---")

    def link(self, fileInfo):
        print("Linking")
        flags = self.solution.exercise.config[self.lang]["linking"]["flags"]
        com = "gcc" if self.lang == "C" else "g++"
        com += " -o out " + " ".join([s + ".o" for s in fileInfo]) + " " + flags
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

class Checker:
    def __init__(self, files: dict):
        self.files = files
        self.asts = self.getAsts()

    def getAst(self, filename):
        fake_libc_include = os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])), 
            'utils', 'fake_libc_include')
        gcc_args = ["-E", f"-I{fake_libc_include}"]
        return parse_file(filename, use_cpp=True, cpp_path="gcc", cpp_args=gcc_args)

    def getAsts(self):
        asts = {}
        for f in self.files:
            asts[f] = self.getAst(f"{f}.c")
        return asts

    class FuncDefVisitor(c_ast.NodeVisitor):
        def visit_FuncDef(self, node):
            t = f"\n{' '*4}"
            print(f"'{node.decl.name}'{t}file: {node.decl.coord.file}"
                f"{t}line: {node.decl.coord.line}{t}column: {node.decl.coord.column}")

    def show_func_defs(self, ast):
        v = self.FuncDefVisitor()
        v.visit(ast)
        
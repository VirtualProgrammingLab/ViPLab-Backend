import os, subprocess, dataObjects
#sys import to put temp dir relative to main.py
#can be removed when that's a fixed absolute path
import sys 
#json import to print "fileInfo" dict in a nice way
# can be removed later
import json
from pycparser import c_parser, c_ast, parse_file

PATH = os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])), "temp")
# Keeps files created in temp folder if DEBUG = True
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
        os.chdir(PATH)
        self.solution = solution
        self.lang = self.solution.exercise.lang
        maxState = self.getMaxState()
        #maxState = 2
        self.replaceCodeWithSolution()
        self.fileext = ".c" if self.lang == "C" else ".cpp"
        print("Merging")
        self.fileInfo = self.merge()
        print(f"fileInfo:\n{json.dumps(self.fileInfo, indent = 2)}")
        print("---")
        if 1 <= maxState:
            print("Compiling")
            self.compile()
            print("---")
        if 2 <= maxState and self.lang == "C":
            print("Checking - WIP")
            self.check()
            print("---")
        if 3 <= maxState:
            print("Linking")
            self.link()
            print("---")
        if 4 <= maxState:
            print("Running")
            self.run()
            print("---")
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
        if len(self.solution.exercise.config[self.lang]["merging"]) == 1:
            return self.mergeSingleFile()
        else:
            return self.mergeMultipleFiles()

    def mergeSingleFile(self) -> dict:
        r = {"temp" : {}}
        code = ""
        loc = 0
        for s in self.solution.exercise.config[self.lang]["merging"]["sources"]:
            for e in self.solution.exercise.elements:
                if s == e["identifier"]:
                    r["temp"][s] = {}
                    r["temp"][s]["visible"] = e["visible"]
                    r["temp"][s]["start"] = (loc + 1)
                    code += e["value"]
                    if not code.endswith("\n"):
                        code += "\n"
                    cnt = e["value"].count("\n")
                    loc += cnt
                    r["temp"][s]["stop"] = loc if cnt != 0 else (loc + 1)
                    break
        loc += 1
        with open(f"temp.{self.fileext}", "w+") as f:
            f.write(code)
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
                        r[fname][s] = {}
                        r[fname][s]["visible"] = e["visible"]
                        r[fname][s]["start"] = (loc + 1)
                        code += e["value"]
                        if not code.endswith("\n"):
                            code += "\n"
                        cnt = e["value"].count("\n")
                        loc += cnt
                        r["temp"][s]["stop"] = loc if cnt != 0 else (loc + 1)
                        break
            loc += 1
            with open(f"{fname}.{self.fileext}", "w+") as f:
                f.write(code)
        return r

    def compile(self):
        files = self.solution.exercise.config[self.lang]["compiling"].get("sources")
        files = files if files is not None else self.fileInfo
        com = f"{self.solution.exercise.getCompilingCommand()} -c "
        com += " ".join([s + self.fileext for s in files])
        print(f"Compiling command: {com}")
        result = subprocess.run(com.split(" "), stdout=subprocess.PIPE)
        print(f"Compiling Output:\n{result.stdout.decode('utf-8')}")

    def check(self):
        checker = Checker(self.fileInfo)
        for a in checker.asts:
            checker.show_func_defs(checker.asts[a])

    def link(self):
        flags = self.solution.exercise.config[self.lang]["linking"]["flags"]
        com = "gcc" if self.lang == "C" else "g++"
        com += f" -o out {' '.join([s + '.o' for s in self.fileInfo])} {flags}"
        print(f"Linking command: {com}")
        result = subprocess.run(com.split(" "), stdout=subprocess.PIPE)
        print(f"Linking Output:\n{result.stdout.decode('utf-8')}")
    
    def run(self):
        os.chmod("out", 0o700)
        com = "./out"
        print("Running command: " + com)
        result = subprocess.run(com.split(" "), stdout=subprocess.PIPE)
        print("Running Output:\n" + result.stdout.decode('utf-8'))

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

    class Visitor(c_ast.NodeVisitor):
        def visit_FuncDef(self, node):
            print(f"File: {node.decl.coord.file}")
            for n in node.body.block_items:
                if isinstance(n, c_ast.FuncCall):
                    print(f"{' '*4}Function: {node.decl.name}\n"
                        f"{' '*8}Function Call: {n.name.name}\n"
                        f"{' '*8}line: {n.coord.line}\n"
                        f"{' '*8}column: {n.coord.column}")

    def show_func_defs(self, ast):
        v = self.Visitor()
        v.visit(ast)
        
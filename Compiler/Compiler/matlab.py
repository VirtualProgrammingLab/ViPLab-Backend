import os, sys, subprocess

PATH = os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])), "temp")
DEBUG = False

class Matlab:
    def __del__(self):
        if os.path.isdir(PATH) and not DEBUG:
            for f in os.scandir(PATH):
                os.remove(f.path)
            print("temp folder cleared")

    def __init__(self, solution):
        print("Language: Matlab\n---")
        if not os.path.exists(PATH):
            os.makedirs(PATH)
            print("created temp folder")

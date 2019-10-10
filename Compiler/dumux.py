import os, subprocess

PATH = "temp"
DEBUG = False

class Dumux:
    def __del__(self):
        if os.path.isdir(PATH) and not DEBUG:
            for f in os.scandir(PATH):
                os.remove(f.path)
            print("temp folder cleared")

    def __init__(self, solution):
        print("Language: DuMuX\n---")
        if not os.path.exists(PATH):
            os.makedirs(PATH)
            print("created temp folder")

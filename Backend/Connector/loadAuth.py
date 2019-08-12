'''
@author: Joshua
'''
def loadAuthenication():
    auth = [0]*6
    ld = open("../UserDB/pinf.passwd","r")
    i = 0
    while i < 6:
        temp = ld.readline()
        pair = temp.split()
        auth[i] = pair[0]
        auth[i+1] = pair[1]
        i = i+2
        temp = ld.readline()
        temp = ld.readline()
        temp = ld.readline()
    return auth
        
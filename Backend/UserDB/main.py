'''
Created on 01.08.2019

@author: Joshua
'''
import os
from UserDB import loadUserDB
from Connector import loadAuth
from Connector import httpConnectCC
from Connector import httpConnectSC
from Connector import httpConnectTC

def main():
    x = loadUserDB.UserDB()
    if os.path.isfile("rsa_key.bin"):
        print("Press [D]ecrypt or [E]ncrypt")
        inp = input().upper()
        if(inp == "D"):
            x.decryptData()
            main2()
        if(inp == "E"):
            x.encryptData("public.pem")         #public.pem of the recieving party

    else:
        print ("else")
        x.genPubKey()
        x.generatePEM()
        
def main2():
    auth = loadAuth.loadAuthenication()
    print("Do you want a [C]omputation Client, [S]tudent Client or [T]eacher Client?")
    if(input().upper() == "C"):
        ConnectorC = httpConnectCC.ConnectCC(auth[4],auth[5])  
        ConnectorC.GetExerciseList()
        ConnectorC.GetSolutions()
        ConnectorC.PostResults() 
        # ConnectorC.GetExercise(ID)  
    if(input().upper() == "S"):
        ConnectorS = httpConnectSC.ConnectSC(auth[2],auth[3])
        ConnectorS.PostSolution()
        ConnectorS.GetResult()
    if(input().upper() == "T"):
        ConnectorT = httpConnectTC.ConnectTC(auth[0],auth[1])
        ConnectorT.postExercise()
        ConnectorT.deleteExercise()
        
        
if __name__ == '__main__':
    main()
'''
@author: Joshua
'''
import os
from UserDB import loadUserDB
from Connector import loadAuth
from Connector import httpConnectCC
from Connector import httpConnectSC
from Connector import httpConnectTC
#Debugging/Presenting Subject To Change
def main():
    x = loadUserDB.UserDB()
    if os.path.isfile("rsa_key.bin"):
        #Decrypt for Controller Interface
        print("Press [D]ecrypt or [E]ncrypt")
        inp = input().upper()
        if(inp == "D"):
            x.decryptData()
            main2()
        if(inp == "E"):
            x.encryptData("reciever.pem")         #public.pem of the recieving party

    else:
        print ("else")
        x.genPubKey()
        x.generatePEM()
        
def main2():
    auth = loadAuth.loadAuthenication()
    print("Do you want a [C]omputation Client, [S]tudent Client or [T]eacher Client?")
    inp = input().upper()
    if(inp == "C"):
        ConnectorC = httpConnectCC.ConnectCC(auth[4],auth[5])  
        ConnectorC.GetExerciseList()
        ConnectorC.GetSolutions()
        #-ConnectorC.PostResults() 
        #ConnectorC.GetExercise(ID)  
    if(inp == "S"):
        ConnectorS = httpConnectSC.ConnectSC(auth[2],auth[3])
        #-ConnectorS.PostSolution()
        ConnectorS.GetResult()
    if(inp == "T"):
        ConnectorT = httpConnectTC.ConnectTC(auth[0],auth[1])
        #-ConnectorT.PostExercise()
        #ConnectorT.GetExercise(ID)
        #ConnectorT.DeleteExercise(ID)
        
        
if __name__ == '__main__':
    main()
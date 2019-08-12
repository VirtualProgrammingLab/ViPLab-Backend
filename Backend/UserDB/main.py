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
    print("Your name is:")
    owner = input().lower()
    if os.path.isfile("rsa_key_"+owner+".bin"):
        #Decrypt for Controller Interface
        print("Press [D]ecrypt or [E]ncrypt")
        inp = input().upper()
        if(inp == "D"):
            x.decryptData(owner)
            main2()
        if(inp == "E"):
            x.encryptData("reciever.pem",owner)         #public.pem of the recieving party

    else:

        x.genPubKey(owner)
        x.generatePEM(owner)
        
def main2():
    escFlag = True
    auth = loadAuth.loadAuthenication()
    while(escFlag):
        print("Do you want a [C]omputation Client, [S]tudent Client or [T]eacher Client? [Q]uit")
        ID = 37
        inp = input().upper()
        if (inp == 'Q'):
           escFlag = False
        if(inp == "C"):
            ConnectorC = httpConnectCC.ConnectCC(auth[4],auth[5])  
            print("GetExercise[L]ist, Get[E]xercise, Get[S]olution or Post[R]esults? [Q]uit")
            cinp = input().upper()
            if (cinp == 'Q'):
                escFlag = False
            if (cinp == 'L'):
                ConnectorC.GetExerciseList()
            if (cinp == 'E'):
                print("Which exercise (ID) to get? Choose from ExerciseList")
                ID = input()
                ConnectorC.GetExercise(ID)  
            if(cinp == 'S'):
                ConnectorC.GetSolutions()
            if (cinp == 'R'):
                ConnectorC.PostResults() 
            
        if(inp == "S"):
            ConnectorS = httpConnectSC.ConnectSC(auth[2],auth[3])
            print("Post[S]olution or Get[R]esults? [Q]uit")
            sinp = input().upper()
            if(sinp == 'Q'):
                escFlag = False
            if (sinp == 'S'):
                ConnectorS.PostSolution()
            if (sinp == 'R'):    
                ConnectorS.GetResult()
        if(inp == "T"):
            ConnectorT = httpConnectTC.ConnectTC(auth[0],auth[1])
            print("Post[E]xercise or [D]eleteExercise? [Q]uit")
            tinp = input().upper()
            if(tinp == 'Q'):
                escFlag = False
            if(tinp == 'E'):
                ConnectorT.PostExercise()
            if(tinp == 'D'):
                print("Which exercise (ID) to delete? Choose from ExerciseList")
                ID = input()
                ConnectorT.DelExercise(ID)
            
        
if __name__ == '__main__':
    main()
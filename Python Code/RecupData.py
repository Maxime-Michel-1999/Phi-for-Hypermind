# -*- coding: utf-8 -*-
"""
Created on Tue Jul  7 12:20:16 2020

@author: maxim
"""

import csv
import numpy as np


def check(X):
    
    #X = RandCcheck()
    
    print("La fonction check fonctionne")
   
    for i in range(np.size(X,0)):
      
        for j in range (np.size(X,0)):
    
            if np.all(X[i]==X[j]) and i!=j :
                
                print("pb de ligne")
                print(i)
                print(j)
                
              
    X = np.transpose(X)
    
    for i in range(np.size(X,0)):
      
        for j in range (np.size(X,0)):
    
            if np.all(X[i]==X[j]) and i!=j :
                
                print("pb de colonne")
                print(i)
                print(j)
    
  
    

def RandCcheck(X):
    
    #This function checks if there is any column or raws that are the same and if needed add noise
    
    #First we check the raws
    
    
    for i in range(np.size(X,0)):
      
        for j in range (np.size(X,0)):
    
            if np.all(X[i]==X[j]) and i!=j :   
                
                 for l in range(np.size(X[i])) : #for each elements of the raw
                        
                        X[i][l]=((X[i][l])*1.001)+(0.00001*i*(X[i][l]))  #It add some noise to the moment of activity (1.001 instead of 1)

    #We do the same thing for the columns
    
    X=np.transpose(X)
        
    for i in range(np.size(X,0)):
      
        for j in range (np.size(X,0)):
    
            if np.all(X[i]==X[j]) and i!=j :
                
                for l in range(np.size(X[i])) : #for each elements of the column
                    
                    X[i][l]=((X[i][l])*1.001)+(0.00001*i*(X[i][l]))  #It add some noise to the moment of activity (1.001 instead of 1)
                
    X = np.transpose(X)
    
    return(X)


def Cov(X):
    covX = np.cov(X)#covariance
    detcovX = np.linalg.det(covX) 
    return(detcovX)


def ComputeX():


    X= []
    IdList= []
    TimeList = []
    n = 0
    m = 0
        
    #First it gather all information about
    with open(r'C:\Users\maxim\Desktop\Stage\Data\SP2K3K.csv') as f:
        reader = csv.reader(f, delimiter = ',')
    
        for row in reader:
            userId = row[3]
            time = row[0]
            type = row[6]
        
        
            if userId not in IdList and userId != '2' and userId != "User ID" and type == 'trade': #On exclue la première colonne est Synt (le robot)
                IdList.append(userId)
                n = n + 1
            if time not in TimeList and userId != '2' and userId != "User ID" and type == 'trade':    
                TimeList.append(time)
                m = m + 1
         
    #Then we build the matrix
    X = np.zeros((n,m))
    
    with open(r'C:\Users\maxim\Desktop\Stage\Data\SP2K3K.csv') as f:
        reader = csv.reader(f, delimiter = ',')
        for row in reader:
        
            time = row[0]
            userId = row[3]
            type = row[6]
        
        
            if userId != '2' and userId != "User ID"  and type == 'trade':
                j = TimeList.index(time) 
                i = IdList.index(userId)
                X[i][j] = 1 
 
    return(X)      
#Le resultat est une matrice ayant comme colonne les "time-step" (donc pour le moment chaque time ou il y un trade)
#les lignes sont les participants (user), avec un 1 si ils étaient actif à ce moment et un 0 sinon.


def ManageData():
     MarketList = [] #List of the different Market Id
     UserLists = [] #List of the Lists of users in each markets
     TimeLists = [] #List of the Lists of timesteps in each markets
     
     with open(r'C:\Users\maxim\Desktop\Git Stage\Phi-for-Hypermind\Trades.csv') as f:
        reader = csv.reader(f, delimiter = ';')
        for row in reader :
            MarketId = row[1]
            if MarketId != 'IFPID' :         
                Time = row[0]
                UserId = row[3]
                Type = row[5]
            
                #First we had the market to the list
                if MarketId not in MarketList and MarketId :
                    MarketList.append(MarketId)
                    UserLists.append([]) #We create a blank space with the same index as in MarketList so that it matchs
                    TimeLists.append([]) #Same
                
                #Then we collect the index of this particular market
                MarketIndex = MarketList.index(MarketId) #This index is valid for each of the 3 lists       
                if UserId != '2' and Type == 'trade' :
                    if Time not in TimeLists[MarketIndex]  :
                        TimeLists[MarketIndex].append(Time)
                    if UserId not in UserLists[MarketIndex] :
                        UserLists[MarketIndex].append(UserId)
            
     #Now we can create the MatrixS
    
     #Let's create the blancks one first
     n = len(MarketList)
     MatrixList = []
     for i in range(n) :
         a = len(TimeLists[i])
         b = len(UserLists[i])
         M = np.zeros((b,a))
         MatrixList.append(M)
        
    
    
    
     with open(r'C:\Users\maxim\Desktop\Git Stage\Phi-for-Hypermind\Trades.csv') as f:
        reader = csv.reader(f, delimiter = ';')
        for row in reader :
            MarketId = row[1]
            if MarketId != 'IFPID' :
                Time = row[0]
                UserId = row[3]
                Type = row[5]
            
                MarketIndex = MarketList.index(MarketId)
                if UserId != '2' and Type == 'trade':
                    j = TimeLists[MarketIndex].index(Time) 
                    i = UserLists[MarketIndex].index(UserId)
                    (MatrixList[MarketIndex])[i][j] = int(1) 
                
     #it returns a package of the 4 lists with corresponding index, Makert, Time, Users, Matrix
     Pack = [MarketList,TimeLists,UserLists,MatrixList]
     return(Pack)
     
def openMarket():
    A = ManageData()
    print('Here are the available markets: ')
    print(A[0])
    MarketNbr = input ("Which one do you want to open ? :  " )
    MarketNbr = str(MarketNbr)
    index = A[0].index(MarketNbr)
    M = A[3][index]
    return(M)

def recupError():
    A= ManageData()
    n = len(A[0])
    ErrorList = [0]*n
    with open(r'C:\Users\maxim\Desktop\Git Stage\Phi-for-Hypermind\BrierScore.csv') as f:
        reader = csv.reader(f, delimiter = ';')
        for row in reader :
            MarketId = row[0]
            if MarketId != 'ï»¿ifpid' :
                Error = row[5]
                index = A[0].index(MarketId)
                ErrorList[index] = float(Error)
                
    return(ErrorList) #This List match the MarketList

            
    
    
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 15 16:21:53 2020

@author: maxim
"""

import numpy as np
import math
import random
import matplotlib.pyplot as plt

def findIndex(m, X): #Enable to find index of a index in a array (in which .index can't be used)
    n = np.size(X)
    for i in range(n):
        v = X[i]
        if v == m :
            return i

def purifyProp(X,p = 0.3):
    
    # This function we'll take out the given pourcentage of the most inactive users
    
    #p = 0.05 #Pourcentage chosen default
    
    nobs = np.size(X[0]) #nombre de colonne (nombre d'observation)
    nall = np.size(X)
    nvar = nall/nobs #nombre de ligne (nombre de user)
    
    nvar = int(nvar)
    nobs = int(nobs)
    
    
    nout = math.floor(nvar*p)
    
    if nout == 0 :
        nout = 1
   
    
    outIndex = np.zeros(nout)
    
    

    outSum = [nobs + 1]*nout

    
    
    #First we select the ones we want to eliminate
    for i in range(nvar):
        sum = 0
        for j in range(nobs):
            sum = X[i][j] + sum
        
        if sum < max(outSum):
            indexMin = findIndex(max(outSum),outSum)
            outSum[indexMin] = sum
            outIndex[indexMin] = i
                
            
    #then we take them out
    
    
    X = np.delete(X,outIndex,0)
    

    return X


def purifyVal(X,v): #Removing user under a certain value v
    nobs = np.size(X,1) #nombre de colonne (nombre d'observation)
    nall = np.size(X)
    nvar = nall/nobs #nombre de ligne (nombre de user)
    
    nvar = int(nvar)
    nobs = int(nobs)
   
    outIndex = []
    
    #First we select the ones we want to eliminate
    for i in range(nvar):
        sum = 0
        for j in range(nobs):
            sum = X[i][j] + sum
        if sum <= v :
            outIndex.append(i)
   
    X = np.delete(X,outIndex,0)
  
    return X

def purifierCheck(X):
    
    nobs = np.size(X[0]) #nombre de colonne (nombre d'observation)
    nall = np.size(X)
    nvar = nall/nobs #nombre de ligne (nombre de user)
    
    nvar = int(nvar)
    nobs = int(nobs)
    
    sumList = []
    List = []
    
    for i in range(nvar):
        sum = 0
        for j in range(nobs):
            sum = X[i][j] + sum
            
        if sum not in sumList :
            List.append([sum,1])
            sumList.append(sum)
        if sum in sumList :
            index =sumList.index(sum)
            List[index][1] =  List[index][1] + 1
            
        
    print(List)  
    
def purifyRowRandom(X,prop = 0.6):
    #This function deletes a certain numer of user chosen randomly

    nvar = np.size(X,0)
    out = math.floor(nvar*prop)
    outList = []
    for i in range(out):
        check = True
        while check == True  :
            r = random.randint(0,nvar-1)
            if r not in outList :
                check = False
                outList.append(r) 
                
    X = np.delete(X,outList,0)   
    return(X)
    
def addColumn(X,n,p = 0.05):
    M = np.zeros((np.size(X,0),np.size(X,1) + n))
    M[:,0:np.size(X,1)] = X
    for i in range(np.size(X,1),np.size(X,1) + n):
        for j in range(np.size(X,0)):
            r = random.uniform(0,1)
            if r > p :
               M[j][i] = 0
            else :
               M[j][i] = 1
    return(M)
    
def purifyNullRow(X):
    n = np.size(X,0)
    outIndex =[]
    for i in range(n):
        if sum(X[i]) == 0 :
            outIndex.append(i)
    X = np.delete(X,outIndex,0)   
    return(X)
            
    
    
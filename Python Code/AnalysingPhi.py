# -*- coding: utf-8 -*-
"""
Created on Mon Jul 20 11:30:34 2020

@author: maxim
"""

from ComputingPhi import ARphiData
from CorrectingData import purifyVal
from CorrectingData import purifyProp
from CorrectingData import addColumn
from CorrectingData import purifyRowRandom
from CorrectingData import purifyNullRow
import numpy as np
import matplotlib.pyplot as plt
import math


def ObsPhiVal(X,n = 7) :
    x = []
    y=[]
    for i in range(n):
        x.append(i)
        try :
            phi = ARphiData(X,1)
        except :
            #That avoid any exception issues
            X = purifyVal(X,i+1)
            x.pop()
               
            
        else :   
            #print("OK")
            if phi < -10 :
                phi = -10
            y.append(phi)
            X = purifyVal(X,i+1)
            
            
    #print(x)
    #print(y)
    
    plt.plot(x,y)
    plt.title("Evolution of Phi")
    plt.grid(b=True, which='major', color='#666666', linestyle='-')
    plt.show()
    
 
def ObsPhiProp(X,n = 98) :
        x = []
        y=[]
        Y = X
        for i in range(30,n):
            p= i/100
            x.append(p)
            #print(i)
            try :
                phi = ARphiData(Y,1)
            except :
                #print("ARphiData n'est pas encore ok")
                Y = purifyProp(X,p)
                x.pop()
            
            else :  
                
                if math.isnan(phi) :
                    x.pop()
                    #print("nan")
                else :
                    y.append(phi)
                Y = purifyProp(X,p)
                #print(p)
                #print(purifierCheck(Y))
                
            
            
        #print(x)
        #print(y)
    
        plt.plot(x,y)
        plt.title("Evolution of Phi")
        plt.grid(b=True, which='major', color='#666666', linestyle='-')
        plt.show()
        
def PhiMean(X,end,p = 0.6):
    start = 0.2
    n = np.size(X,1)
    start = math.floor(n*start)
    end = math.floor(n*end)
    PhiList=[]
    step = math.ceil((end-start)/10)
    for i in range(start,end,step):
        M = X[:,:i]
        M = purifyNullRow(M) #Take of the user that aren't active for the moment
        M = purifyProp(M,p) 
        try :
            phi = ARphiData(M,1)
        except:
            pass
        else:
            if phi < 0 : phi = 0
            if math.isnan(phi) or math.isinf(phi) :
                pass
            else: PhiList.append(phi)
                   
    mean = sum(PhiList)/len(PhiList)
    return(mean)
    
def ObsPhiNodes(X):
    
    phiList = []
    lenList = []
    
    X = purifyProp(X,0.6) 
    
    for i in range(10,60):
        prop = i/100
        A = purifyRowRandom(X,prop)
        phi = ARphiData(A,1)
        phiList.append(phi)
        lenList.append(np.size(A,0))
        
    plt.plot(lenList,phiList)
    plt.title("Correlation Phi Len")
    plt.grid(b=True, which='major', color='#666666', linestyle='-')
    plt.show()
        

def ObsPhiColumn(X):
     
    phiList = []
    lenList = []
    
    X = purifyProp(X,0.6)
    
    for i in range(30):
        A = addColumn(X,i)
        phi = ARphiData(A,1)
        phiList.append(phi)
        lenList.append(np.size(A,1))
        
    plt.plot(lenList,phiList)
    plt.title("Correlation Phi Obs")
    plt.grid(b=True, which='major', color='#666666', linestyle='-')
    plt.show()
    

def ObsZerosColumn(X):
    
    pList = []
    cList = []
    
    for i in range(np.size(X,1)):
       C = X[:,i]
       p = sum(C)/(np.size(C))
       pList.append(p)
       cList.append(i)
    
    plt.plot(cList,pList)
    plt.title("Prop of zeros per column")
    plt.grid(b=True, which='major', color='#666666', linestyle='-')
    plt.show()
        
        
def PhiEv(X):
    #This function wil allow us to follow the evolution of phi following time
    
    start = 20 #♣This is the time step at which we start mesuring
    phiList =[]
    timestepList = []
    nobs=np.size(X,1)
    p=0.6
    print("We eliminate ",p*100, "% of the most inactive users")
    for i in range(start,nobs):
        Y = X [:,:i]     
        Y = purifyProp(Y,p)
        timestepList.append(i)
        
        try :
            phi = ARphiData(Y,1)
        except : 
            timestepList.pop()
        else :  
            if math.isnan(phi) or math.isinf(phi):
                    timestepList.pop()      
            else :
                    phiList.append(phi)
                
    
    plt.plot(timestepList,phiList,'b')
    plt.title("Evolution of Phi")
    plt.grid(b=True, which='major', color='#666666', linestyle='-')
    plt.yscale("log")         
    plt.show()
    



# -*- coding: utf-8 -*-
"""
Created on Thu Jul  9 11:53:33 2020

@author: maxim
"""

from ComputingPhi import ARphiData
from RecupData import ComputeX
from RecupData import openMarket
from RecupData import recupError
from RecupData import ManageData
from CorrectingData import purifyProp
from CorrectingData import purifyNullRow
import math
import matplotlib.pyplot as plt
import numpy as np
from AnalysingPhi import ObsPhiProp
from AnalysingPhi import PhiMean
from AnalysingPhi import PhiEv
from scipy.stats import linregress
import csv
import os

def ComputePhi():
    
    X = ComputeX()
    
    #X = RandCcheck(X) It doesn't seem necessary
   
    Treshold = input ("Value of the Activity Treshold ? (We advise more than 0.5) : " )
    Treshold = float(Treshold)
    
    X = purifyProp(X,Treshold)   
    Phi = ARphiData(X)   
    return(Phi)
    

    
    
def StudyMarket():
    M = openMarket()
    print("Time Evolution of Phi")
    PhiEv(M)
    print("Evolution of Phi at the end of the market following purification")
    ObsPhiProp(M)
    
def StudyMarkets(): #print all the evolution of phi for every market 
    A = ManageData()
    for i in range(len(A[0])):
        M = A[3][i]
        PhiEv(M)
    
def StudyPhi():
    A = ManageData()
    ErrorList = recupError()
    PhiList = []
    MarketList = A[0]
    PopList = []
    ObsList = []
    n = len(A[0])
    prop = input("How much do you want to purify : (between 0 and 1) ")
    p = float(prop)
    
    #The result of this input needs to be between 0 ans 1 (Maybe some other time we'l make it more adaptable)
    answ = input(" Mean / Prop / Timestep  ?  : ")
    if answ == 'Mean' :
        step = input("At what step do you want to study phi ? (Proportion of complete market duration) : ")
        step = float(step)
        for i in range(n) :
            print(i)
            M = A[3][i]
            mean = PhiMean(M,step,p)
            PhiList.append(mean)
        
    if answ == 'Timestep' : 
        ErrorListsorted = [] #To select the market that can be use in this case (obs > step)
        MarketListsorted =[]
        TotPopList = []
        step = input("At what step do you want to study phi ? (What timestep) : ")
        step = int(step)
        for i in range(n):
            M = A[3][i]         
            if np.size(M,1) > step : 
                M = purifyNullRow(M[:,:step])
                l= np.size(M,0)
                M = purifyProp(M, p)
                try :
                    phi = ARphiData(M)
                except:
                    pass
                else :
                    if phi < 0 : phi = 0
                    if math.isnan(phi) or math.isinf(phi) :  
                        pass
                    else :
                        PhiList.append(phi)
                        ErrorListsorted.append(ErrorList[i])
                        MarketListsorted.append(MarketList[i])
                        PopList.append(np.size(M,0))
                        TotPopList.append(l)
                    
                    
        ErrorList=ErrorListsorted
        MarketList = MarketListsorted
        l = len(ErrorList)
        
        
    elif answ == 'Prop' :
        ErrorListsorted = []
        MarketListsorted =[]
        step = input("At what step do you want to study phi ? (Proportion of complete market duration) : ")
        step = float(step)
        for i in range(n) :
            M = A[3][i]
            Len = math.floor((np.size(A[3][i],1))*step)
            M = M[:,:Len]
            M = purifyNullRow(M)
            l= np.size(M,0)
            M = purifyProp(M,p)
            try :
                phi = ARphiData(M,1)
            except : 
                pass
            else :
                if phi < 0 : phi = 0
                if math.isnan(phi) or math.isinf(phi) :  
                    pass
                else :
                    PhiList.append(phi)
                    ErrorListsorted.append(ErrorList[i])
                    MarketListsorted.append(MarketList[i])
                    PopList.append(np.size(M,0))
                    TotPopList.append(l)
                    
            
        ErrorList = ErrorListsorted   
        MarketList = MarketListsorted
        
    #The list need to be sort
    for k in range(1,np.size(ErrorList)):
        temp=ErrorList[k]
        temp2=PhiList[k]
        temp3=MarketList[k]
        temp4=PopList[k]
        temp5=TotPopList[k]
        j=k
        while j>0 and temp<ErrorList[j-1]:
            ErrorList[j]=ErrorList[j-1]
            PhiList[j]=PhiList[j-1]
            MarketList[j] = MarketList[j-1]
            PopList[j]=PopList[j-1]
            TotPopList[j]=TotPopList[j-1]
            j-=1
        ErrorList[j]=temp
        PhiList[j]=temp2
        MarketList[j]=temp3
        PopList[j]=temp4
        TotPopList[j]=temp5
    
    #Regression Linéaire
    
    slope, intercept, rvalue, p_value, std_err =  linregress(ErrorList,PhiList)

    
    def predict(X):
        Y = [i*slope for i in ErrorList]
        return(Y + intercept)
    
    fitline = predict(ErrorList)
    plt.plot(fitline,ErrorList, color = 'red')
    plt.scatter(PhiList,ErrorList)
    plt.title("Correlation Phi Error")
    #plt.grid(b=True, which='major', color='#666666', linestyle='-')
    plt.xlabel('Phi Value')
    plt.ylabel('Brier Score')
    Rcoeff = round(rvalue,3)
    plt.figtext(0.7,0.7, Rcoeff, fontsize='xx-large')
    plt.show()
    
    print("The determination coefficient is : ", rvalue)
    
    return(ErrorList,PhiList,MarketList,PopList,TotPopList,p,step)

def savePhiData():
    A = StudyPhi()
    ErrorList = A[0]
    PhiList = A[1]
    MarketList = A[2]
    PopList = A[3]
    TotPopList = A[4]
    p = A[5]
    step = A[6]
    
    Initial = ['BrierScore','MarketId','Total Users','User Removed %','Users Left','Step','Phi']
    
    with open(r'C:\Users\maxim\Desktop\Git Stage\Phi-for-Hypermind\Results\DataMatrix.csv','w',newline='') as f:
        thewriter = csv.writer(f,delimiter = ';')  
        
        #First We write the headers
        thewriter.writerow(Initial)
        
        #Then we file it with information 
        for i in range(np.size(ErrorList)):
            
            Row = [ErrorList[i],MarketList[i],TotPopList[i],p*100,PopList[i],step,PhiList[i]]
            thewriter.writerow(Row)
               
            
def bestRvalue():
        A = ManageData()
        ErrorList = recupError()
        finalR = 0
        n = len(A[0])
        I,J = 0,0
        for i in range(30,70,10): #purification
            p = i/100
            stepList = []
            RList = []
            NumberMarket = []
            for j in range(40,400,10) : #step
                step = j
                ErrorListsorted = []
                PhiList=[]
                stepList.append(step)
                for l in range(n) :
                    M = A[3][l]
                    #Len = math.floor((np.size(A[3][l],1))*step)
                    if np.size(M,1) > step :
                        M = M[:,:step]
                        M = purifyNullRow(M)
                        M = purifyProp(M,p)
                        try :
                            phi = ARphiData(M,1)
                        except : 
                            pass
                        else :
                            if phi < 0 : phi = 0
                            if math.isnan(phi) or math.isinf(phi) :  
                                pass
                            else :
                                PhiList.append(phi)
                                ErrorListsorted.append(ErrorList[l])
                    
            
                Errors = ErrorListsorted
                if len(Errors)< 10 :
                    stepList.pop()
                    continue
                #The list need to be sort
                for k in range(1,np.size(Errors)):
                    temp=Errors[k]
                    temp2=PhiList[k]
                    m=k
                    while m>0 and temp<Errors[m-1]:
                        Errors[m]=Errors[m-1]
                        PhiList[m]=PhiList[m-1]
                        m-=1
                    Errors[m]=temp
                    PhiList[m]=temp2

                #Regression Linéaire
    
                slope, intercept, rvalue, p_value, std_err =  linregress(Errors,PhiList)
                
                RList.append(abs(rvalue))
          
                if abs(rvalue) > finalR : 
                    finalR = abs(rvalue)
                    I = i
                    J = j
                    ErrorsF = Errors
                    phi = PhiList
                    
                NumberMarket.append(len(Errors)) #That will give us the number of market that could be used for computation
            
            print(p,"% of the users have been removed")
            m = sum(RList)/len(RList)
            Mean = [m]*len(RList)
            plt.plot(stepList,Mean,color='red')
            plt.scatter(stepList,RList)
            plt.title("Evolution of the Correlation Coefficient ")
            plt.grid(b=True, which='major', color='#666666', linestyle='-')
            plt.xlabel('Timestep')
            plt.ylabel('Correlation Coefficient')
            plt.show()
            
            print("The number of market considered for this plot is :", NumberMarket )
                            
        return(I,J,finalR)

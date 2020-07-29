# -*- coding: utf-8 -*-
"""
Created on Tue Jul  7 11:52:58 2020

@author: maxim
"""
import numpy as np
from numpy import matlib as matlib
import math
from RecupData import check
import warnings

#X is the data matrix, rows correspond to elements, columns to observations.
# tau is the number of lags over which to compute ARPhi

def reversedata(X, nobs, nvar):
    
    v = int(nvar)
    o = int(nobs)
    

    Y = np.zeros((v,o))    
    for i in range(o) :
        for j in range(v) :
            Y[j][i] = X[j][nobs-i-1]
    
    return(Y)

    

def changeColumn(X,Y,i) :
    #this function allows to change a column of a matrix by using its transpose
    
    Xt = np.transpose(X) 
    Xt[i] = Y
    return(np.transpose(Xt))
    
    

def ARphiData(X, tau = 1) : 
    #Number of elements in system and number of observation
    
    
    nobs = np.size(X[0]) #nombre de colonne (nombre d'observation)
    nall = np.size(X)
    nvar = nall/nobs #nombre de ligne (nombre d'élément)
    
    nvar = int(nvar)
    nobs = int(nobs)
    tau = int(tau)

    #if(nvar>nobs): 
    #    print("error in ARphidata : nvar>nobs , check input data") #C'est pas vraiment necessaire ca
        
    #Time-reverse the data (inversion of column) 
    
    X = reversedata(X,nobs,nvar)
    
    #Variables contained in bipartition (not used for our "atomic" partition)
    
    #remove sample means if present (not interested in constant terms in regressions)
    
    m = np.mean(np.transpose(X), axis = 0)
    if(abs(sum(m))>0.0001):
        mall = matlib.repmat(m,nobs,1)
        X = X - np.transpose(mall)
    
    
    
    
    
    
    #Regression of present of X to predict past of X
    
    
    regressors = np.zeros((nobs-tau,nvar)) #Tau being the current moment so the 'present' of X
    
    for i in range(nvar) :
        for j in range(nobs-tau):
            regressors[j][i] = X[i][j]
        
    beta = np.zeros((nvar,nvar))
    xpred = np.zeros((nobs-tau,nvar))
    u = np.zeros((nobs-tau,nvar))
    
    for i in range(nvar) :  
        xvec = np.transpose(X[i])
        xdep = xvec[tau:]
        beta = changeColumn(beta,(np.linalg.lstsq(regressors,xdep,rcond=None))[0],i)#It changes the i column of beta        
        xpred = changeColumn(xpred,np.transpose(((np.transpose(beta))[i]).dot(np.transpose(regressors))),i) #allow to have a product with a column, transpose of a product is the product of transposes
        u = changeColumn(u,np.transpose(xdep) - np.transpose(xpred)[i],i) #residuals of X

           
    covResX = np.cov(np.transpose(u))
    detResX = np.linalg.det(covResX)  

    
    #Regression de X
    covX = np.cov(X)                #covariance
    detcovX = np.linalg.det(covX)   #Determinant
    
    
    
    
    
    
    #cov and det for each part (atomic partition)
    
    covParts = []    #List of the "partition" covariances
    detParts = []    #Liste of the det for each
    
    for j in range(nvar) :         
        
        covParts.append(np.cov(X[j]))
        detParts.append(covParts[j])
        #We conseider that the det of a sclar is the scalar so we don't need to compute it
        
    
    #det and cov of residuals for each parts
    
    covRes = []    #List of the "partition's residuals" covariances
    detRes = []    #Liste of the det for each
    
    #Need to check the dimension
    mpred = np.zeros((nobs - tau,1))
    u = np.zeros((nobs - tau,1))
    
    for l in range(nvar):
        
        regressor = np.zeros((nobs-tau,1))
        for i in range(nobs-tau):
            regressor[i]=X[l][i]
        mvec = np.transpose(X[l])
        mdep = mvec[tau:]
        beta = np.linalg.lstsq(regressor,mdep,rcond=None)[0]
        mpred = regressor.dot(beta)
        u = mdep - mpred
           
        
        #We can now had the covariance and det to the list
        
        covRes.append(np.cov(u))
        detRes.append(covRes[l]) #With our partition we don't compute de det, we just keep the covariance.
        
     
    
    #Calculate effective information 
    #First we compute the sum
    
    
 
    sumParts = 0
    for j in range (nvar) :
        #let's cheat to avoid the issue of dividing by zero (which happen once in the first example)
        if detRes[j] != 0 :
            sumParts = sumParts + (1/2)*math.log(detParts[j]/detRes[j]) #WARNING, the cooefficient 1/2 need to be meditate, it mabe only suited for the 2 terms sum
    
    #print("Value of the second term : ", sumParts)
    warnings.filterwarnings("ignore") #That just erase the warnings on the console
    phi = (1/2)*math.log(detcovX / detResX) - sumParts
    #print(phi)
    
    #Normalisation factor
    
    
    normParts = []
    for j in range(nvar) : #Warning, if we change from atomic to larger partition this formula needs revision
        normPart = (1/2)*math.log((2*math.pi*math.exp(1))*detParts[j]) #same question with de coefficient, is it suited for 2 parts ? or does it works with nvar of them
        normParts.append(normPart)
        
     
    norm=min(normParts)
    #Normalised effective information
    
    phinorm = phi / norm

   
    # print("La valeur de Phi est :")
    return(phi)
    
    

    
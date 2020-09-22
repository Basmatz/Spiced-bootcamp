# -*- coding: utf-8 -*-
"""
Created on Sun Sep 20 23:16:52 2020

@author: Besitzer
"""


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.decomposition import NMF
#
#
#-----------------------------------------------------------------------------#
#MovieLens data downloaded from
#https://grouplens.org/datasets/movielens/
path = 'C:/Alex/SPICED/week10/ml-latest-small/'
fileName = 'ratings.csv'
features=20
#no. of iterations
niter=100
#-----------------------------------------------------------------------------#
#
#
def pq(P,Q,A,alpha):    
    
    
    ''' calculates next P,Q using coordinate descent:
    see https://archive.siam.org/meetings/sdm11/park.pdf (slide 13)
    alpha enhances convergence behaviour'''
    
    
    
    PP = np.dot(P.T,P)
    QQ = np.dot(Q,Q.T)
    PQQ = np.dot(P,QQ)
    PPQ = np.dot(PP,Q)
    AQ = np.dot(A,Q.T)
    PA = np.dot(P.T,A)
    PPQ=np.dot(P.T,np.dot(P,Q))    
    #     
    for i in range(0,P.shape[0]):
        for j in range(0,P.shape[1]):  
            P[i,j]=P[i,j]+(alpha/QQ[j,j])*(AQ[i,j]-PQQ[i,j])
            #if Pnew[i,j]<0: Pnew[i,j]=0    
           
    for i in range(0,Q.shape[0]):
        for j in range(0,Q.shape[1]):
             Q[i,j]=Q[i,j]+(alpha/PP[i,i])*(PA[i,j]-PPQ[i,j])
             #if Qnew[i,j]<0: Qnew[i,j]=0                      
    return P,Q


def getMatrix(pathFileName,fna):     
    df = pd.read_csv(pathFileName)   
    M=df.drop(['timestamp'],axis=1)
    M=M.set_index(['userId','movieId'])
    M_stack=M['rating'].unstack(0)
    M_stack.fillna(fna,inplace=True)
    ##transpose matrix (movieID x userID has shown better convergence)
    return M_stack.T
    
if __name__ == '__main__': 
    #A : rows: USER_ID, cols: MOVIE_ID
    A = getMatrix(path+fileName,2.).to_numpy()
    A = A[:50,:250] 
    
    #use Sklearn   
    m = NMF(n_components=features,max_iter=niter,init='random',verbose=0,tol=1e-3)  
    m.fit(A)
    # 
    #use pq function
    #initial random P and Q matrices
    P = np.random.randint(1,10, size=(A.shape[0], features)).astype('float')
    Q = np.random.randint(1,10, size=(features,A.shape[1])).astype('float') 
    
    #array to store norm for all iteration
    itnorm = np.zeros(niter+1) 
    for i in range(niter+1):
        P,Q = pq(P,Q,A,.05)
        Anew=np.dot(P,Q)       
        itnorm[i] = np.linalg.norm(A-Anew,ord='fro' )   
    #
    #
    #plot norm at each iteration and compare with norm returned by sklearn.NMF
    plt.figure(figsize=(16,7))
    plt.plot(itnorm,color='b',label='fro norm of my algorithm') 
    #plot norm calculated by sklearn 
    plt.plot([0,niter],[m.reconstruction_err_,m.reconstruction_err_],color='r',ls='--',
             label= f'sklearn fro norm after {niter} iteration' )    
    plt.tick_params(axis='y', which='minor', direction='out')     
    #plt.yscale('symlog')   
    plt.grid(True, which="both", ls="-")
    plt.xlabel('no. of iterations')
    plt.ylabel(r'$\|\| \mathbf{A}-\mathbf{PQ} \|\|_{F} $')
    plt.title('My NMF Algorithm Convergence (Frobinus Norm)', fontsize=20)
    plt.legend()
    plt.show()  
    #
    print (f'sklearn Frobenius Norm: {m.reconstruction_err_.round()}')
from numba import jit
from numba import prange
import numpy as np
import random

@jit(nopython=True)
def branching(nw,wconf,zeta):
    #nw=nwaker,wconf[i]=WeightOfWalker[i],zeta[0:nw-1]=walkersrandnumber,zeta[nw]=randnumber
    surv=0 #survived walkers initialize
    histw=np.zeros(nw)
    jbra=np.zeros(nw)
    weight=np.sum(np.abs(wconf))

    if weight==0: #check
        print("Error: sum of walker weights is 0!")
        return jbra,weight,surv,histw

    for i in range(nw): #update of random number into z[:]. "zeta[nw]" contains a random number.
        zeta[i]=weight*(zeta[nw]+i)/nw

    zeta[nw]=2*weight #In this way I am sure that zeta[nw]>wsumB because wsumB<=weight
    pos=0
    wsumA=0

    for i in range(nw):
        wsumB=wsumA+np.abs(wconf[i])
        cont=0
        while(pos < nw and zeta[pos]<wsumB and zeta[pos]>=wsumA):
            jbra[pos]=i
            pos+=1
            histw[i]+=1 #number of walker clones
        wsumA=wsumB
        if (histw[i]!=0): #if there are copies of the walkers
            surv+=1 #then increase the survive walker index

    weight=weight/nw #average of the weight
    if(pos!=nw): #check
        print("Error")

    wconf[:]=1 #reset to 1
    return jbra,weight,surv,histw

@jit(nopython=True)
def upjbra(nw,jbra,histw): #here I permute the walkers in a way that I can use reshuffle in a cheap way
    #histw=np.zeros(nw)
    killw=np.zeros(nw) #I store the killed walkers here

    #for i in range(nw): #Sorella nel suo codice lo calcola di nuovo, ma possiamo usare quello calcolato nel branching
    #    histw[int(jbra[i])]+=1

    posk=0 #number of killed walkers
    for i in range(nw):
        if(histw[i]==0): #if i-th walker is dead
            killw[posk]=i #I store its position
            posk+=1
    pos=0
    for j in range(nw): #I know histw[i] therefore I am able to build a permutation.
        if(histw[j]!=0):
            jbra[j]=j
            for i in range(1,int(histw[j])):
                jbra[int(killw[pos])]=j
                pos+=1
    return jbra

@jit(nopython=True)
def reshuff(nw,jbra,iconf,tab,diag,bx,el):
    for i in range(nw):
        ind=jbra[i]
        if (i != ind):
            iconf[:,i]=iconf[:,ind]
            tab[:,i]=tab[:,ind]
            diag[i]=diag[ind]
            bx[i]=bx[ind]
            el[i]=el[ind]
    return


'''
nw=10 #Example
zeta=np.zeros(nw+1)
zeta[nw]=np.random.rand()
wconf=5*np.ones(nw)*np.random.rand(nw)
jbra,weight,surv,histw= branching(nw,wconf,zeta)
print(jbra)
jbra=upjbra(nw,jbra,histw)
print(jbra)
'''

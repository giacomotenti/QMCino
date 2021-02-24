from numba import jit
from numba import prange
import numpy as np
import random

@jit(nopython=True)
def dmc_heis(conf,tab,el,diag,bx,nit):
    for i in range(int(nit)):
        for w in range(nw):
            W[w]*=bx[w]
            r=random.random()
            gn=np.zeros(L+1)
            gn[0]=Lambda-diag[w]
            for j in range(L):
                if tab[w,j]: gn[j+1]=0.5
            ztry=r*np.sum(gn)
            ntry=gn[0]
            iout=-1
            while(ntry<ztry):
                iout+=1
                ntry+=gn[iout+1]
                if iout>L:
                    print('molto male')
                    break
            jout=np.mod(iout+1, L)
            if iout!=-1:conf[w,iout]=not(conf[w,iout])
            if iout!=-1:conf[w,jout]=not(conf[w,jout])
            tab[w], el[w], diag[w]=update(conf[w],tab[w],iout,el[w],diag[w])
            bx[w]=(Lambda-el[w])/(L* (np.log(2.0) - 0.25))
    return conf
<<<<<<< HEAD

@jit(nopython=True)
def branching(nw,wconf,nrand):
    #nw=nwaker,wconf[i]=WeightOfWalker[i],zeta[0:nw-1]=walkersrandnumber,zeta[nw]=randnumber
    surv=0 #survived walkers initialize
    histw=np.zeros(nw)
    jbra=np.zeros(nw)
    weight=np.sum(np.abs(wconf))
    zeta = np.zeros(nw+1)
 #   if weight==0: #check
 #       print("Error: sum of walker weights is 0!")
 #       return jbra,weight,surv,histw

    for i in range(nw): #update of random number into z[:]. "zeta[nw]" contains a random number.
        zeta[i]=weight*(nrand+i)/nw

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
 #   if(pos!=nw): #check
 #       print("Error")
    #I add this part so that branching subroutine does all the dirty work
    jbra = upjbra(nw,jbra,histw)
    iconf, tab, diag , bx, el = reshuff(nw,jbra,iconf,tab,diag,bx,el)
    return iconf,tab, diag, bx , el,weight, surv

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
    return iconf,tab,diag,bx,el
=======
>>>>>>> 3b1bd75d1ad286b2a5e2ed59fdd9b51fb9193513

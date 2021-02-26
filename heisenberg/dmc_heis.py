import numpy as np
import time
from numba import jit, njit , prange
from heisenberg.update import update, computetab

#main loop
def run_dmc_heis(L,nit,nbra,nw):
    t0 = time.time()
    print('DMC algorithm on a {} site 1d Heisenberg model'.format(L))
    print('Starting calculation with {} walkers'.format(nw))
    print('Branching each {} steps.'.format(nbra))
    surv_sum = 0
    f = open('dmc_heis.dat','w')

    #initialization:
    conf_0 = np.empty(L,dtype='bool')
    for site in range(L):
        if site % 2 == 0:
            conf_0[site] = True
        else:
            conf_0[site] = False
    conf = np.tile(conf_0,(nw,1))
    tab_0 = np.empty(L,dtype='bool')
    tab_0 , bx_0 , el_0 , diag_0 = computetab(tab_0,conf_0,L)
    tab = np.tile(tab_0,(nw,1))
    bx = bx_0*np.ones(nw)
    el = el_0*np.ones(nw)
    diag = diag_0*np.ones(nw)
    #end initialization

    #loop on the number of branchings
    for istep in range(nit):
        conf , tab,  weight , energy, el, diag, bx, surv = dmc_heis(L,nw,conf,tab,bx,el,diag,nbra)
        surv_sum += surv
        f.write('{:.16f} \t {:.16f} \t {} \n'.format(istep, energy, weight))
        if 10*(istep+1) % nit == 0:
            print('{}% completed'.format(100*(istep+ 1)//nit))
    f.close()
    print('Data written in dmc_heis.dat')
    surv_sum = surv_sum / (nw * nit)
    print('Average survived walkers after branching = {:.5f}'.format(surv_sum))
    t1 = time.time()
    print('Elapsed time = {} s'.format(t1-t0))


@njit(parallel=True)
def dmc_heis(L,nw,conf,tab,bx,el,diag,nsteps):
#accumulated weight initialized to one
    wconf = np.ones(nw)
    Lambda = L / 4.0
#parallelized loop on walkers
    for i in range(nsteps):
        for w in prange(nw):
            #accumulate the weight
            wconf[w]*=bx[w]
            #random move
            r=np.random.rand()
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
            #non diag move if iout != -1
            if iout!=-1:
                conf[w,iout]=not(conf[w,iout])
                conf[w,jout]=not(conf[w,jout])
                tab[w], bx[w] , el[w], diag[w] = update(conf[w],tab[w],iout,el[w],diag[w])
    #energy weighted average before branching
    energy = np.sum(el*wconf)/np.sum(wconf)
    #here we call the branching
    nrand = np.random.rand()
    jbra,weight, surv = branching(nw,wconf,nrand)
    conf, tab, diag, bx, el = reshuff(nw, jbra, conf, tab, diag, bx, el)
    return conf, tab,  weight , energy , el, diag, bx, surv

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
    return jbra,weight, surv

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
def reshuff(nw,jbra,conf,tab,diag,bx,el):
    for i in range(nw):
        ind =int(jbra[i])
        if (i != ind):
            conf[i]=conf[ind]
            tab[i]=tab[ind]
            diag[i]=diag[ind]
            bx[i]=bx[ind]
            el[i]=el[ind]
    return conf,tab,diag,bx,el

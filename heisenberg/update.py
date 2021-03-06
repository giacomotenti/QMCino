import numpy as np
from numba import jit ,njit , prange


@njit(parallel=False)
def computetab(tab,conf,L):
    Lambda = L / 4.0
    #lambda - ground state energy (see Bethe ansatz)
    e0 = Lambda+L* (np.log(2.0) - 0.25)
    diag = 0
    el = 0
    for i in range(L):
        j = np.mod(i+1, L)
        if conf[i]!= conf[j]:
            tab[i] =True
            el = el - 0.5
            diag = diag - 0.25
        else:
            diag = diag + 0.25
            tab[i] =False # no move is possible
    el+=diag
    bx=Lambda-el
    return  tab, bx/e0, el, diag

@jit(nopython=True)
def update(conf,tab,iout,el,diag):
    L=conf.shape[0]
    Lambda=L/4.0
    e0 =Lambda+ L* (np.log(2.0) - 0.25)
    #diag=0
    iback=np.mod(iout-1,L)
    if conf[iback]!= conf[iout]:
        tab[iback] =True
        el = el - 1
        diag = diag - 0.5
    else:
        diag = diag + 0.5
        tab[iback] =False # no move is possible
        el+=1
    jout=np.mod(iout+1,L)
    ifor=np.mod(jout+1,L)
    if conf[ifor]!= conf[jout]:
        tab[jout] =True
        el -= 1
        diag -= 0.5
    else:
        diag += 0.5
        tab[jout] =False # no move is possible
        el+=1
    #el+=diag
    bx=Lambda-el
    return   tab, bx / e0,  el,diag

#example
#L=4
#tab=np.empty(L,dtype=bool)
#
#conf=[np.mod(i,2)==0 for i in range(L)]
#conf=np.array(conf,dtype=bool)
#print("stato=",conf)
#bx,tab,el,diag=computetab(tab,conf,L)
#print("diag",diag)
#print("tab iniziale=",tab)
#print("energia locale= ",el)
#iout=0
#conf[0]=np.invert(conf[0])
#conf[1]=np.invert(conf[1])
#
#print("configurazione post",conf)
#print("tab, el e diag= ",update(conf,tab,iout,el,diag))

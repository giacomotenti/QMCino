#from numba import jit
#from numba import boolean
import numpy as np
#from heisenberg.wavefun import psi


#@jit(nopython=True)
def computetab(conf,L):
    Lambda = L / 4.0
    e0 = L* (np.log(2.0) - 0.25)
    diag = 0
    el = 0
    tab=np.empty(L,bool)
    for i in range(L):
        j = np.mod(i+1, L)
        if conf[i]!= conf[j]:
            tab[i] =True
            el = el - 0.5#i segni sono giusti?
            diag = diag - 0.25
        else:
            diag = diag + 0.25
            tab[i] =False # no move is possible
    el+=diag
    bx=Lambda-el
    return bx/e0 , tab, el
#@jit(nopython=True)
def update(conf,tab,iout,el):
    L=conf.shape[0]
    Lambda=L/4.0
    e0 = L* (np.log(2.0) - 0.25)
    diag=0
    iback=np.mod(iout-1,L)
    if conf[iback]!= conf[iout]:
        tab[iback] =True
        el = el - 1
        diag = diag - 0.5
    else:
        diag = diag + 0.5
        tab[iback] =False # no move is possible
        el+=1
    ifor=np.mod(iout+1,L)
    if conf[ifor]!= conf[iout]:
        tab[iout] =True
        el = el - 1
        diag = diag - 0.5
    else:
        diag = diag + 0.5
        tab[iout] =False # no move is possible
        el+=1
    el+=diag
    bx=Lambda-el
    return bx/e0 , tab, el

#example
#
#L=4
#conf=[np.mod(i,2)==0 for i in range(L)]
#conf=np.array(conf,dtype=bool)
#print("stato=",conf)
#bx,tab,el=computetab(conf,L)
#print("tab iniziale=",tab)
#print("energia locale= ",el)
#iout=1
#conf[iout]=np.invert(conf[iout])
#print("configurazione post",conf)
#print(update(conf,tab,iout,el))

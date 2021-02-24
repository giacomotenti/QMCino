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

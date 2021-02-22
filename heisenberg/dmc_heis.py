from numba import jit
from numba import prange
import numpy as np
import random

@jit(nopython=True)
def dmc_heis(conf,nit):
    #L=4
    #la=L/4.
    #nw=1
    #diag=-1
    #tab=np.array((True, True, True, True))
    for i in range(nit):
        for w in range(nw):
            r=random.random()
            gn=np.zeros(L+1)
            gn[0]=la-diag
            for j in range(L):
                if tab[j]: gn[j+1]=0.5
            ztry=r*np.sum(gn)
            ntry=gn[0]
            iout=-1
            while(ntry<ztry):
                iout+=1
                ntry+=gn[iout+1]
                print(iout, ntry, ztry)
                if iout>L:
                    print('molto male')
                    break
            jout=np.mod(iout+1, L)
            if iout!=-1:conf[iout]=not(conf[iout])
            if iout!=-1:conf[jout]=not(conf[jout])
            #update....
        return conf

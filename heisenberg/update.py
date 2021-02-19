from numba import jit
import numpy as np
from heisenberg.wavefun import psi

@jit(nopython=True)
def update(conf,tab,L):
    Lambda = L / 4.0
    e0 = L* (np.log(2.0) - 0.25)
    #...

    return bx/ e0 , tab
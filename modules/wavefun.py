import numpy as np
from numba import jit

@jit(nopython=True)
def psi(x,alpha,L,which):
   if which == 0:
       if x<1 or x>L:
           return 0
       else:
           return 1
   if which == 1:
       if x < 1 or x > L:
           return 0
       else:
           return np.exp( - alpha * x)
  # if which == 2:
  #     if x<1 or x > L:
  #         return 0
  #     else:
  #         return np.exp(- alpha[0]*x) * x**alpha[1]

#WAVEFUNCTION FOR HEISENBERG MODEL
#def marsh

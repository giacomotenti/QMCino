from numba import jit
from modules.wavefun import psi

@jit(nopython=True)
def update(x,alpha,t,t2,V,L,which):
    Lambda = V * L
    psix = psi(x,alpha,L,which)
    psi_l = psi(x-1,alpha,L,which)
    psi_r = psi(x+1,alpha,L,which)
    psi_l2 = psi(x-2,alpha,L,which)
    psi_r2 = psi(x+2,alpha,L,which)
    vsf = t2 * (psi_l2 + psi_r2) / psix
    bx = -V * x - vsf + Lambda + t * (psi_l + psi_r) /psix
    elx = -t * (psi_l + psi_r) /psix + vsf + V * x
    P_left = t * psi_l / psix / bx
    P_right = t * psi_r /psix / bx
    return bx / Lambda , elx , P_left , P_right


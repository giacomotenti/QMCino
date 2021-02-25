import numpy as np
from numba import jit, njit ,prange
import time
from modules.update import update
import random as rand

@jit(nopython=True)
def E_dmc_mod(alpha,t,t2,V,L,which,n_it,x0):
    x = x0
    bx , elx , P_left , P_right = update(x,alpha,t,t2,V,L,which)
    #weights are set to one
    w=1
    for i in range(n_it):
        y = rand.random()
        #weight at one step back
        b_old = bx
        if y < P_left:
            x -= 1
            bx , elx , P_left , P_right = update(x,alpha,t,t2,V,L,which)
        elif y < P_left + P_right:
            x += 1
            bx , elx , P_left , P_right = update(x,alpha,t,t2,V,L,which)
        w *= b_old
    return x, w, elx

@jit(nopython=True)
def branching(x_w, w_w, nw):
    # branching!
    y = np.random.rand()
    prob = (w_w / np.sum(w_w))
    x_out= np.empty(nw)
    j = 0
    prob_sum = prob[0]
    for i in range(nw):
        z = (i + y) / nw
        while z > prob_sum:
            j += 1
            prob_sum += prob[j]
        x_out[i] = x_w[j]
    return x_out

@njit(parallel=True)
def propagate(alpha,t,t2,V,L,which,nbra,nw,xxx,wwalker):
    el = np.zeros(nw)
    wwalker = np.zeros(nw)
    for w in prange(nw):
        xxx[w], wwalker[w], el[w] = E_dmc_mod(alpha, t, t2, V, L,which, nbra, xxx[w])
    weight = np.mean(wwalker)
    energy = np.sum(el * wwalker)/np.sum(wwalker)
    pos = np.sum(xxx * wwalker)/np.sum(wwalker)
    xxx_out = branching(xxx, wwalker, nw)
    return xxx_out , pos , energy , weight

def run_mw(alpha,t,t2,V,L,which,nbra,nit,nw):
    t0 = time.time()
    xxx = np.ones(nw)
    wwalker = np.ones(nw)
    f = open('dmc_branch.dat', 'w')
    f.write('# mean_posi \t mean_energy \t mean_weight \n' )
    print('running parallel mode')
    for ij in range(nit):
        xxx , pos , energy ,weight = propagate(alpha,t,t2,V,L,which,nbra,nw,xxx,wwalker)
        f.write('{:.16f} \t {:.16f} \t {} \n'.format(pos, energy, weight))
        if 10*(ij+1) % nit == 0:
            print('{}% completed'.format(100*(ij+ 1)//nit))
    f.close()
    print('Data written on dmc_branch.dat')
    t1 = time.time()
    print('Elapsed time = {} s'.format(t1-t0))
    return

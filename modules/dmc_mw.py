import numpy as np
import multiprocessing as mp
import time
from modules.update import update
import random as rand

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

def branching(x_w, w_w):
    nw = np.size(x_w)
    # branching!
    y = np.random.rand()
    prob = (w_w / np.sum(w_w))
    x_out= np.empty(nw)
    for i in range(nw):
        z = (i + y) / nw
        j = 0
        prob_sum = prob[0]
        while z > prob_sum:
            j += 1
            prob_sum += prob[j]
        x_out[i] = x_w[j]
    return x_out

def run_mw(alpha,t,t2,V,L,which,nbra,nit,nw,parallel):
    t0 = time.time()
    xxx = np.ones(nw)
    wwalker = np.ones(nw)
    el = np.zeros(nw)
    f = open('dmc_branch.data', 'w')
    f.write('# mean_posi \t mean_energy \t mean_weight \n' )
    if (parallel):
        npool = mp.cpu_count()
        print('running parallel mode')
        print('parallelize on {} cores'.format(npool))
    else:
        print('running serial mode')
    for ij in range(nit):
        if (parallel):
            pool = mp.Pool(npool)
            res = []
            for w in range(nw):
                res.append(pool.apply_async(E_dmc_mod, args=(alpha, t, t2, V, L,which, nbra, xxx[w])))
            pool.close()
            pool.join()
            w = 0
            for i in res:
                xxx[w], wwalker[w], el[w] = i.get()
                w += 1
        else:
            for w in range(nw):
                xxx[w], wwalker[w], el[w] = E_dmc_mod(alpha, t, t2, V, L,which, nbra, xxx[w])
        weight = np.mean(wwalker)
        energy = np.sum(el * wwalker)/np.sum(wwalker)
        pos = np.sum(xxx * wwalker)/np.sum(wwalker)
        xxx = branching(xxx, wwalker)
        f.write('{:.16f} \t {:.16f} \t {} \n'.format(pos, energy, weight))
        if 10*(ij+1) % nit == 0:
            print('{}% completed'.format(100*(ij+ 1)//nit))
    f.close()
    print('Data written on dmc_branch.dat')
    t1 = time.time()
    print('Elapsed time = {} s'.format(t1-t0))
    return

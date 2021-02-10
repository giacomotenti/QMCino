import numpy as np
import time
from modules.update import update
import random as rand

def E_dmc(alpha,t,t2,V,L,which,n_it,x0):
    #single walker technique
    t0 = time.time()
    x = x0
    f = open('dmc.dat','w')
    bx , elx , P_left , P_right = update(x,alpha,t,t2,V,L,which)
    for i in range(n_it):
        if 10*(i+1) % n_it == 0:
            print('{}% completed'.format(100*(i+ 1)//n_it))
        y = rand.random()
        #weight at one step back
        b_old = bx
        if y < P_left:
            x -= 1
            bx , elx , P_left , P_right = update(x,alpha,t,t2,V,L,which)
            f.write(str(x) + '\t' + str(elx) + '\t' + str(b_old) + '\n')
        elif y < P_left + P_right:
            x += 1
            bx , elx , P_left , P_right = update(x,alpha,t,t2,V,L,which)
            f.write(str(x) + '\t' + str(elx) + '\t' + str(b_old) + '\n')
        else:
            f.write(str(x) + '\t' + str(elx) + '\t' + str(b_old) + '\n')
    f.close()
    t1 = time.time()
    print('Data written on ./dmc.dat')
    print('Elapsed time = {} s'.format(t1-t0))

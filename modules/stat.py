import numpy as np
import time
from numba import jit

def dmc_stat(bin_dim,bin0,pmax,filename,xyes = True):
    t0 = time.time()
    f = open(filename,'r')
    data = f.readlines()
    d = []
    for line in data:
        if line.partition('#')[0] == '':
            continue
        dlist = [float(x.strip('\n')) for x in line.split('\t')]
        d.append(dlist)
    data_array = np.array(d)
    t1 = time.time()
    print(filename + ' read in {} s'.format(t1-t0))
    res = stat_calc(data_array,bin_dim,bin0,pmax)
    E = res[0]
    sE = res[1]
    x = res[2]
    sx = res[3]
    with open('dmc_en.dat','w') as out:
        for i in range(pmax):
            out.write('{}\t{}\t{}\t{}\t{}\n'.format(i+1,E[i],sE[i],x[i],sx[i]))
    print('Energy = {} +/- {}'.format(E[-1],sE[-1]))
    if xyes:
        print('Position = {} +/- {}'.format(x[-1],sx[-1]))
    tfin = time.time()
    print('Total time = {} s'.format(tfin - t0))
    f.close()

@jit(nopython=True)
def stat_calc(data_array,bin_dim,bin0,p):
    count = 0
    nmeas = 0
    E = np.zeros(p)
    E2 = np.zeros(p)
    x = np.zeros(p)
    x2 = np.zeros(p)
    Ebin = np.zeros(p)
    xbin = np.zeros(p)
    Gnp = np.zeros(p)
    Gpbin = np.zeros(p)
    Gtot = np.zeros(p)
    G2tot = np.zeros(p)
    wlist = np.zeros(p)
    xlist = np.zeros(p)
    for dat in data_array:
        if count >= p:
            if count >= bin0*bin_dim :
                if count % bin_dim == 0 and count != bin0*bin_dim:
                    E += Ebin
                    E2 += Ebin**2 / Gpbin
                    x += xbin
                    x2 += xbin**2 / Gpbin
                    Gtot += Gpbin
                    G2tot += Gpbin**2
                    Ebin = np.zeros(p)
                    Gpbin = np.zeros(p)
                    xbin = np.zeros(p)
                    nmeas += 1
                Gnp[p-1] = np.prod(wlist)/wlist[0]
                xbin[p-1] += Gnp[p-1]*xlist[-p//2]
                for indp in range(p-2,-1,-1):
                    Gnp[indp] = Gnp[indp+1]/wlist[p-indp-1]
                    xbin[indp] += Gnp[indp]*xlist[-(indp+1)//2]
                Ebin += dat[1]*Gnp
                Gpbin += Gnp

            wlist = np.append(wlist,dat[2])
            wlist = wlist[1:]
            xlist = np.append(xlist,dat[0])
            xlist = xlist[1:]
        else:
            wlist[count] = dat[2]
            xlist[count] = dat[0]
        count += 1
    E/=Gtot
    E2/=Gtot
    x/= Gtot
    x2/= Gtot
    #SigmaE = np.sqrt((E2 - E**2) / (1 - G2tot / Gtot**2))
    #Sigmax = np.sqrt((x2 - x**2) / (1 - G2tot / Gtot**2))
    SigmaE = np.sqrt((E2 - E**2) / (nmeas -1 ))
    Sigmax = np.sqrt((x2 - x**2) / (nmeas -1 ))
    return ( E , SigmaE , x , Sigmax)

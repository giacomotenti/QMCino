import os
import sys
import argparse
import numpy as np
from modules import wavefun as wf
from modules import dmc_sw
from modules import stat
from modules import dmc_mw

#GLOBAL VARIABLES
t = 1
t2 = 0
V = 5
L = 30
alpha = 1.0
which = 1

def change():
    print('Set new parameters for the Hamiltonian:')
    global t , t2 , V , L , alpha , which
    inp = input('t? ')
    t = float(inp)
    inp = input('t2? ')
    t2 = float(inp)
    inp = input('V? ')
    V = float(inp)
    inp = input('L? ')
    L = int(inp)


def echo_param():
    global L , t , t2 , V , alpha , which
    print(' L  = {}'.format(L))
    print(' t  = {}'.format(t))
    print(" t' = {}".format(t2))
    print(' V  = {}'.format(V))
    if which == 0:
        print('Constant wavefunction (no parameters!)')
    elif which == 1:
        print('Exponential wavefunction (one parameter)')
        print('Alpha = {}'.format(alpha))
    elif which == 2:
        print('Wavefunction x^beta * exp(-alpha * x)')
        print('Alpha = {}'.format(alpha[0]))
        print('Beta = {}'.format(alpha[1]))

def readinput(file):
    global L , t , t2 , V , alpha , which
    inp = {}
    inp['L'] = L
    inp['t'] = t
    inp['t2'] = t2
    inp['V'] = V
    inp['alpha'] = alpha
    inp['which'] = which
    inp['calc'] = 'dmc'
    inp['opt'] = 'parallel'
    inp['nsteps'] = 100000
    inp['nbra'] = 10
    inp['nw'] = 100
    with open(file,'r') as f:
        for x in f.readlines():
            xx = x.partition('#')[0]
            entry =[l.strip(' \t\n') for l in xx.partition('=') if l.strip()]
            if entry != []:
                if entry[0] in inp:
                    inp[entry[0]] = entry[2]
    L = int(inp['L'])
    t = float(inp['t'])
    t2 = float(inp['t2'])
    V = float(inp['V'])
    alpha = float(inp['alpha'])
    which = int(inp['which'])
    return (inp['calc'],inp['opt'],int(inp['nsteps']),int(inp['nbra']),int(inp['nw']))

def main(args):
    global L , t , t2 , V , alpha , which
    if args.input == 'null':
        print('Welcome in')
        logo = ( '   #####  ##   ##  #####        # #    #  ####\n \
 #     # # # # # #     #       # ##   # #    #\n \
 #     # #  #  # #             # # #  # #    #\n \
 #   # # #     # #        ###  # #  # # #    #\n \
 #    #  #     # #     #       # #   ## #    #\n \
  #### # #     #  #####        # #    #  #### ')
        print(logo)
        print('')
        explain_commands = 'Type: \n \
        -echo_param: show parameters of the Hamiltonian; \n \
        -set_param: set the parameters of the Hamiltonian; \n \
        -set_fun: change the guiding/variational function \n \
        -opt: optimize the parameters in the wavefunction \n \
        -vmc: calculate vmc energy and observables \n \
        -dmc: calculate fn energy and observables\n \
        -read_dmc: post processing for dmc \n \
        -quit (q): exit'
        print(explain_commands)
        while True:
            inp = input('>>>').strip(' ')
            if inp == 'quit' or inp == 'q':
                break
            elif inp == 'echo_param':
                echo_param()
            elif inp == 'set_param':
                change()
                echo_param()
            elif inp == 'set_fun':
                wftype_try= int(input('How many parameters (0,1,2)?'))
                if wftype_try >= 0 and wftype_try < 3:
                    which = wftype_try
                    if which == 1:
                        alpha = float(input('Value of alpha? ').strip(' '))
                    elif which ==2:
                        alpha = np.zeros(2)
                        alpha[0] = float(input('Value of alpha? ').strip(' '))
                        alpha[1] = float(input('Value of beta? ').strip(' '))
                else:
                    print('Wrong number!')
            elif inp == 'dmc':
                print('Starting dmc calculation with fixed node approximation.')
                print('Current parameters:')
                echo_param()
                print('Which algorithm? \n \
        -sw: single walker (standard algorithm) \n \
        -mw: many walkers (branching with fixed population)')
                inp = input('>>>').strip(' ')
                if inp == 'sw':
                    n_it = int(input('How many steps? ').strip(' '))
                    x0 = int(input('Initial position of the walker? ').strip(' '))
                    dmc_sw.E_dmc(alpha,t,t2,V,L,which,n_it,x0)
                elif inp == 'mw':
                    nit = int(input('Number of branchings? ').strip(' '))
                    nbra = int(input('nbra? ').strip(' '))
                    nw = int(input('# of walkers? ').strip(' '))
                    par_run = input('Run in parallel?(yes/no)').strip(' ')
                    if par_run == 'yes' or par_run == 'y':
                        parallel = True
                    elif par_run == 'no' or par_run == 'n':
                        parallel = False
                    else:
                        print('Bad option!')
                    dmc_mw.run_mw(alpha,t,t2,V,L,which,nbra,nit,nw,parallel)
                else:
                    print('Bad option!')
            elif inp == 'read_dmc':
                if os.path.exists('./dmc.dat'):
                    filename = 'dmc.dat'
                    print('Data read from ./dmc.dat')
                    bindim = int(input('Bin dimension: ').strip(' '))
                    bin0 = int(input('Initial bin for averages: ').strip(' '))
                    p = int(input('Projection length: ').strip(' '))
                    stat.dmc_stat(bindim,bin0,p,filename)
                else:
                    print('dmc.dat does not exist')
            else:
                print(inp + ' command not found')
                print(explain_commands)
    else:
        if os.path.exists(args.input):
            inputfile=args.input
            inparam = readinput(inputfile)
            echo_param()
            print('Starting ' + inparam[0] )
            if inparam[0].strip(' ') == 'dmc':
                if inparam[1].strip(' ') == 'serial':
                    print('Running serial algorithm')
                    if inparam[4] == 1:
                        dmc_sw.E_dmc(alpha,t,t2,V,L,which,inparam[2],1)
                    else:
                        dmc_mw.run_mw(alpha,t,t2,V,L,which,inparam[3],inparam[2],inparam[4],False)
                if inparam[1].strip(' ') == 'parallel':
                    print('Running parallel algorithm')
                    dmc_mw.run_mw(alpha,t,t2,V,L,which,inparam[3],inparam[2],inparam[4],True)
            else:
                print('Not a supported option!')
        else:
            print('Error:  ' + args.input + ' does not exist')
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--input' , type = str , help = 'input file',default = 'null')

    args = parser.parse_args()
    main(args)

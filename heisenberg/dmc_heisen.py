#modules

def dmc_heis(conf,nit):
    #MC move
    #genera un random
    #se mosse non diagonale call update


#jbra ?
@jit(nopython=True)
def branching(x_w, w_w, nw):
    # branching!
    y = np.random.rand()
    prob = (w_w / np.sum(w_w))
    x_out = np.empty(nw) #non necessario? Prova a implementare upjbra e reshuff
    j = 0
    prob_sum = prob[0]
    for i in range(nw):
        z = (i + y) / nw
        while z > prob_sum:
            j += 1
            prob_sum += prob[j]
        x_out[i] = x_w[j]
    return x_out


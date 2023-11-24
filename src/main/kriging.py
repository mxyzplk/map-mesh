from pykrige.ok import OrdinaryKriging
import matplotlib.pyplot as plt
import pykrige.kriging_tools as kt
import numpy as np

# memory allocation problems
def kriging(ix, iy, ip, ox, oy):
    
    nn = 10
    ngo = len(ox)
    ngi = len(ix)
    di = np.empty(ngi)
    lowest = np.empty(nn)
    res = []
    
    for i in range(ngo): # for each output grid  
    
        di = calc_distances(ox[i], oy[i], ngi, ix, iy)
        lowest = get_n_lowest(di, nn)
        
        ok = OrdinaryKriging(ix[lowest.astype(int)], iy[lowest.astype(int)], ip[lowest.astype(int)], variogram_model="linear", verbose=False, enable_plotting=False)                         
    
        z, ss = ok.execute("grid", ox, oy)
    
        z_res = np.ravel(z)
        
        res.append(z_res)
    
    return res


def calc_distances(a1, a2, ng, g1, g2):

    d = np.empty(ng)
    
    for i in range(ng):
        d1 = a1 - g1[i]
        d2 = a2 - g2[i]
        d[i] = (d1 ** 2 + d2 ** 2) ** 0.5

    return d
    
       
     
def get_n_lowest(arr, n):
        if n <= 0:
            return []
    
        sorted_indices = np.argsort(arr)
    
        return sorted_indices[:n]  

    


    
    
    
    
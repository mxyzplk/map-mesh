import numpy as np
import os


class IDWInterpolator:
    def __init__(self, ng, power, nearest):
        self.ng = int(ng)
        self.g = np.empty((self.ng, 2))
        self.v = np.empty(self.ng)
        self.d = np.empty(self.ng)
        self.w = np.empty(self.ng)
        self.e = int(nearest)
        self.power = float(power)


    def set_mesh(self, a1, a2, a3):
        self.g[:, 0] = a1[:]
        self.g[:, 1] = a2[:]        
        self.v[:] = a3[:]
        
    
    def idw(self, a1, a2, n):
        self.calc_distances(a1, a2)
        lowest = self.get_n_lowest(self.d, int(n))
        
        sum1 = 0
        sum2 = 0
        for i in range(int(n)):
            sum1 = sum1 + self.w[int(lowest[i])] * self.v[int(lowest[i])]
            sum2 = sum2 + self.w[int(lowest[i])]
        res = sum1 / sum2
        return res
            
    
    
    def eval_mesh(self, grids, plane, ng):
        res = np.empty(int(ng))
        for i in range(ng):
            if (int(plane) == 0):       # plane xy
                res[i] = self.idw(grids[i, 0], grids[i, 1], self.e)
            
            elif (int(plane) == 1):     # plane xz
                res[i] = self.idw(grids[i, 0], grids[i, 2], self.e)
        return res
    
    
    def calc_distances(self, a1, a2):

        for i in range(self.ng):
            d1 = a1 - self.g[i, 0]
            d2 = a2 - self.g[i, 1]
            self.d[i] = (d1 ** 2 + d2 ** 2) ** 0.5
            self.w[i] = 1 / ((self.d[i] + 1e-10) ** self.power)

            
            
    def get_n_lowest(self, arr, n):
        if n <= 0:
            return []
    
        sorted_indices = np.argsort(arr)
    
        return sorted_indices[:n]
    
    
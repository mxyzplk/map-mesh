from pykrige.ok import OrdinaryKriging
import matplotlib.pyplot as plt
import pykrige.kriging_tools as kt
import os

# memory allocation problems
def kriging(ix, iy, ip, ox, oy, resultdir, fout):
    
    ok = OrdinaryKriging(ix, iy, ip, variogram_model="linear", verbose=False, enable_plotting=False)                         
    
    z, ss = ok.execute("grid", ox, oy)
    
    fg_i = fout.replace(".txt", "_i.png")
    fg_o = fout.replace(".txt", "_o.png")
    
    r1 = os.path.join(resultdir, fout)
    r2 = os.path.join(resultdir, fg_i)
    r3 = os.path.join(resultdir, fg_o)
    
    plt.imshow(z, extent=(min(ox), max(ox), min(oy), max(oy)), origin='lower', cmap='viridis')
    plt.savefig(r3)
    
    plt.imshow(ip, extent=(min(ix), max(ix), min(iy), max(iy)), origin='lower', cmap='viridis')
    plt.savefig(r2)


    
    
    
    
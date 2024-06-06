'''
Created on 2024/04/28

@author: coutakagi
'''
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde

def plotXY(outfn,x,y):    
    _, ax = plt.subplots()
    _=ax.scatter(x, y)
    plt.savefig(outfn)
    plt.close()
    
def plotXY_density(sz,outfn,x,y, lb):
    #sz = (0,1): figsize (x,y), 2:labelsize 3: subplot left
    xy = np.vstack([x,y])
    plt.rcParams['xtick.labelsize'] = sz[2]
    plt.rcParams['ytick.labelsize'] = sz[2]

    fig, ax = plt.subplots(figsize=(sz[0], sz[1]))
    
    try:
        z = gaussian_kde(xy)(xy)
        im=ax.scatter(x, y, c=z,cmap="jet",s=5)
    except:
        
        im=ax.scatter(x, y,s=5)

    ax.set_xlabel(lb[0])
    ax.set_ylabel(lb[1])

#    cb=fig.colorbar(im, orientation="horizontal")
    cb=fig.colorbar(im, orientation="horizontal",pad=0.2)
#    cb.ax.tick_params(labelsize=sz[2])
    cb.ax.tick_params(labelsize=6)
    
    fig.tight_layout()
    if sz[3]>0:
        fig.subplots_adjust(left=sz[3])
#        fig.subplots_adjust(left=sz[3], bottom=sz[3])
    
    plt.savefig(outfn)
    plt.close()
  
    
    
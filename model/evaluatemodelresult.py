'''
Created on 2024/04/28

@author: coutakagi
'''
import numpy as np
from scipy.stats import pearsonr
from utlplot import plotXY

def evalprediction(pmat, sigset):
    sig_t=sigset[0]
    sig_ans=sigset[1]
    prv=getpredval(pmat, sig_t)
    corval=evalcorrelation(prv,sig_ans)
    return corval, prv

def evalprediction_node(pmat, sigset):
    sig_t=sigset[0]
    sig_ans=sigset[1]
    prv=getpredval(pmat, sig_t)
    corval_node=evalcorrelation_node(prv,sig_ans)
    return corval_node

def evalprediction_plot(outfn,pmat, sigset):
    ""
    #evaluate model and plot correlation
    corval, predictions=evalprediction(pmat, sigset)
    sig_ans=sigset[1]
    plotXY(outfn,sig_ans, predictions)
    return corval, predictions
    
def evalprediction_XY(pmat, sigset):
    ""
    #evaluate model and plot correlation
    _, predictions=evalprediction(pmat, sigset)
    sig_ans=sigset[1]
    ret_xy=[]
    ans=np.reshape(sig_ans,(-1))
    ret_xy.append(ans)
    prd=np.reshape(predictions,(-1))
    ret_xy.append(prd)
    return ret_xy
    


def getpredval(pmat, sigt):
    r=np.matmul(pmat, sigt.T)
    r=r.T
    return r
    
def evalcorrelation( x0, y0):
    x=np.reshape(x0, (-1))
    y=np.reshape(y0, (-1))
    ret=pearsonr(x,y)[0]
    return ret
def evalcorrelation_node(dtx0, dty0):
    ret=[]
    #dtx  =[time, node]
    n = dtx0.shape[1]
    for i in range(n):
        x0=dtx0[:,i]
        y0=dty0[:,i]
        x=np.reshape(x0, (-1))
        y=np.reshape(y0, (-1))
        pret=pearsonr(x,y)[0]
        ret.append(pret)
    ret=np.array(ret)
    return ret
        
        
    
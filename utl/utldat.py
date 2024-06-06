'''
Created on 2024/04/28

@author: coutakagi
'''
import numpy as np

def appendlist(ret, dt):
    for d in dt:
        ret.append(d)
    return ret

def liststr(dt):
    ret=""
    for i, d in enumerate(dt):
        ret+=str(d)
        if i<len(dt)-1:
            ret+="_"
    return ret


def settextfromlist(vlist):
    ret=""
    for v in vlist:
        if isinstance(v, float):
            ret+="{:.5f}\t".format(v)
        else:
            ret+=str(v)
            ret+="\t"
    return ret

def getresultStandarderrors(yb,xb,dt0):
    #x=np.array(dt0).shape[0]
    #y=np.array(dt0).shape[1]
    ret=[]
    for i, d in enumerate(dt0):
        if i>=xb:
            pret=[]
            for j, dy in enumerate(d):
                if j>=yb:
                    pret.append(dy)
            ret.append(pret)
    ret=np.array(ret, dtype=np.float32)
    n=ret.shape[0]
    ns=np.sqrt(n)
    if ns==0:
        ns=1
#    ret=np.mean(ret, axis=0)
    rets=np.std(ret, axis=0)
    rets=rets/ns
#    print("se dims = {}\t {} \t {} ".format(ret.shape, n, rets.shape))
    return rets

def getresultAverages(yb,xb,dt0):
    #x=np.array(dt0).shape[0]
    #y=np.array(dt0).shape[1]
    ret=[]
    for i, d in enumerate(dt0):
        if i>=xb:
            pret=[]
            for j, dy in enumerate(d):
                if j>=yb:
                    pret.append(dy)
            ret.append(pret)
    ret=np.array(ret, dtype=np.float32)
    ret=np.mean(ret, axis=0)
    return ret
        
    
    


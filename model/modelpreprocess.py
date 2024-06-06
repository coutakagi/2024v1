'''
Created on 2024/04/28

@author: coutakagi
'''
import numpy as np


def preproc_normalizesignal(sig0):
    standardize_type=0#default (signal -region average)/ -1 = raw data
    ret=preproc_standardizesignal(standardize_type,sig0)
    return ret

def preproc_normalizesignal_runningaverage(sig0, window_size):
    standardize_type=0#default (signal -region average)/ -1 = raw data
    ret=preproc_standardizesignal(standardize_type,sig0)
    if window_size>1:
        ret=avr_window(window_size, ret)

    return ret

def avr_window(ws, s0):
    ret=[]
    tr=s0.shape[0]
    nn=s0.shape[1]
    wn=ws
    if wn==0:
        wn=1
    for t in range(tr-ws):
        r=np.zeros(nn)
        for p in range(ws):
            r+=s0[(t+p),:]
        r=r/wn
        ret.append(r)
    ret=np.array(ret)
    return ret

 
def preproc_standardizesignal(standardize_type,sig0):
    if standardize_type==0:#avr
        sp0=normsigav(sig0)
    if standardize_type==-1:#raw
        sp0=sig0
    return sp0
   

def splittrainingdat(sig0, rt):
    #get data for training and validation and prepare answer (s(t) and s(t+1))
    #sig0 = signal data
    #rt = ratio for validation data
    intv=1#time interval for answer (default 1: t -> t+1)
    st_0,st1_0=splitdat_trainingandanswer(sig0, intv)
    n_time=len(st_0)#number of time
    n_trn, _=splitnumber(n_time,rt)
    rp=np.random.permutation(n_time)
    pos_trn=rp[0:n_trn]
    pos_val=rp[n_trn:n_time]
    sig_trn=[st_0[pos_trn,:],st1_0[pos_trn,:]]
    sig_val=[st_0[pos_val,:],st1_0[pos_val,:]]
    return sig_trn, sig_val


def splittrainingdat_intv(sig0, rt, intv):
    #get data for training and validation and prepare answer (s(t) and s(t+1))
    #sig0 = signal data
    #rt = ratio for validation data
#    intv=1#time interval for answer (default 1: t -> t+1)
    st_0,st1_0=splitdat_trainingandanswer(sig0, intv)
    n_time=len(st_0)#number of time
    n_trn, _=splitnumber(n_time,rt)
    rp=np.random.permutation(n_time)
    pos_trn=rp[0:n_trn]
    pos_val=rp[n_trn:n_time]
    sig_trn=[st_0[pos_trn,:],st1_0[pos_trn,:]]
    sig_val=[st_0[pos_val,:],st1_0[pos_val,:]]
    return sig_trn, sig_val
    

def resetInterval(sig_val, intv):
    sig0=sig_val[0]

    st_0,st1_0=splitdat_trainingandanswer(sig0, intv)

    ret=[st_0,st1_0]
    return ret
    

def splitnumber(n_time,rt):
    if rt>=1.0 or rt<0.0:
        rt=0.1#set default
    n1=n_time*rt
    n1=np.round(n1)
    n1=int(n1)
    n0=n_time-n1
    return n0, n1

def splitdat_trainingandanswer(sig0, intv):
    ret=[]
    retan=[]
    for i in range(len(sig0)-intv):
        t=sig0[i,:]
        a=sig0[i+intv,:]
        ret.append(t)
        retan.append(a)
    ret=np.array(ret)
    retan=np.array(retan)
    return ret, retan    



def normsigav(sigt0):
    ret=setavr(sigt0)
    return ret


def setavr(sig):
    pret=setavr0(sig.T)
    ret=pret.T
    return ret

def setavr0(sig):
    a=np.mean(sig, axis=1)
    ret=[]
    for s,aa in zip(sig,a):
        s=s-aa
        ret.append(s)
    ret=np.array(ret)
    return ret






'''
Created on 2024/04/27

@author: coutakagi
'''
import os 
import pathlib
import numpy as np
import pandas as pd

def getfilelistinfol(fol, ftype):
    ""
    #get file list in folder "fol", ftype = file type = "csv". "gz", etc
    ft="**/*."+ftype
    p_temp = pathlib.Path(fol)
    flist= p_temp.glob(ft)
    ret=[]
    flist=list(flist)
    for f in flist:
        f=os.path.abspath(f)
        ret.append(f)
    return ret


def addfol(path0, sb):
    #append sub folder to path (if not exist -> create folder) 
    path0=checkfol(path0)
    ret=os.path.join(path0, sb)
    ret=checkfol(ret)
    return ret

def checkfol(path):
    #check folder if exists
    if not os.path.exists(path):
        os.mkdir(path)
    path=os.path.abspath(path)
    path+="/"
    return path 


def getfilebasename(f0, outfol):
    #get file name without file extension
    from pathlib import Path
    f=Path(f0)
    fn0=os.path.basename(f)
    fn=fn0.split(".")[0]
    ret=os.path.join(outfol, fn)
    return ret, fn


def savefilenpcsv(dt0, fn):
    # save data as numpy csv file
    dt=np.array(dt0)
    np.savetxt(fn,dt,delimiter=",")

def savefilenpcsv_str(dt0, fn):
    # save string data as numpy csv file
    #with string
    
    try:
        dt=np.array(dt0)
        np.savetxt(fn,dt,delimiter=",",fmt = "%s")
    except:
        ""

def loadfilenpcsv(fn):
    return np.loadtxt(fn,delimiter=",")

def loadfilenpcsv_str(fn):
    try:
        df = pd.read_csv(fn, header=None)
        ret=np.array(df)
        return ret
    except:
        return None

def getdatanames4defaultdat(dname):
    sps=dname.split("_")
    sub=sps[0]
    ses=sps[1]
    tsk0=""
    flg=0
    for sp in sps:
        if "bold" in sp:
            flg=1
        if flg==0:
            tsk0=sp
    sub=getcontentname(sub)
    ses=getcontentname(ses)
    
    ret=[sub,ses,tsk0]
    return ret
    
def getcontentname(tsk0):
    tsk=""
    sps_tsk=tsk0.split("-")
    for i, st in enumerate(sps_tsk):
        if i>0:
            tsk+=st
        if i<len(sps_tsk)-1 and i>0:
            tsk+="-"
    return tsk
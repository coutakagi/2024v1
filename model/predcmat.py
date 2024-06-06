'''
Created on 2024/04/28

@author: coutakagi
'''
import os
from utlfiles import addfol, getdatanames4defaultdat
from prepimg2sig import signaldata

from modelpreprocess import preproc_normalizesignal, splittrainingdat,\
    preproc_normalizesignal_runningaverage
from evaluatemodelresult import evalprediction
from trainingmodel import exetraining

from utlfiles import savefilenpcsv_str, savefilenpcsv, loadfilenpcsv
from utldat import appendlist, liststr

def exeprediction(param):
    ""
    ret=[]
    fol_input0=param.fol_input#input image folder
    fol_input_dat=addfol(fol_input0,param.dataname)
    outfol0=param.fol_output#output folder
    outfol0=addfol(outfol0,"signal")
    dat_categories = param.subfol_img# rest/task
    for dat_category in dat_categories:
        fol_input=addfol(fol_input_dat,dat_category)
        outfol=addfol(outfol0,dat_category)
        #load/create signal time series data from fMRI images
        signaldats=signaldata(fol_input,outfol,param)
#        pret=getPredictModeltrainingv2()
        pret=predictModelmatrix(param,dat_category,signaldats)
        ret.append(pret)
    return ret

def exeprediction_runningaverage(param, window_sizes):
    ""
    ret=[]
    fol_input0=param.fol_input#input image folder
    fol_input_dat=addfol(fol_input0,param.dataname)
    outfol0=param.fol_output#output folder
    outfol0=addfol(outfol0,"signal")
    dat_categories = param.subfol_img# rest/task
    for dat_category in dat_categories:
        fol_input=addfol(fol_input_dat,dat_category)
        outfol=addfol(outfol0,dat_category)
        #load/create signal time series data from fMRI images
        signaldats=signaldata(fol_input,outfol,param)
#        pret=getPredictModeltrainingv2()
#        pret=predictModelmatrix(param,dat_category,signaldats)
        pret=predictModelmatrix_runningaverage(window_sizes,param,dat_category,signaldats)
        ret.append(pret)
    return ret


def predictModelmatrix(param,dat_category,signaldats):
    num_test=param.num_test#number of files to test
    outfol0=param.fol_output#output folder
    outfol0=addfol(outfol0,"predict")
    outfol=addfol(outfol0,"matrix")
    outfol=addfol(outfol,dat_category)
    #dat_category = rest/task (default)
    
    result_record=[]
    rec_fn=os.path.join(outfol0,"result_"+dat_category+".csv")


    for i, sdat in enumerate(signaldats):
        if num_test==-1 or i< num_test:
            sig0=sdat[0]
            datname0=sdat[2]#file name and path
            #data contents of default data (rest/task, task names etc)
            datname=getdatanames4defaultdat(datname0)
            f_sbn="file_"+str(i)
            output_f=addfol(outfol,f_sbn)
            sig=preproc_normalizesignal(sig0) 
            modelres=trainingmodel(sig,param, output_f,datname)
            pret=[f_sbn]
            pret=appendlist(pret,datname)
            pret=appendlist(pret,modelres)
            pret.append(datname0)
            result_record.append(pret)
            savefilenpcsv_str(result_record,rec_fn)

def predictModelmatrix_runningaverage(window_sizes,param,dat_category,signaldats):
    
    outfol0p=param.fol_output#output folder
    outfol0p=addfol(outfol0p,"predict_ravr")
    for window_size in window_sizes:
        outfol0=addfol(outfol0p,"ws_"+str(window_size))
        predictModelmatrix_ravexe(window_size,outfol0,param,dat_category,signaldats)
        


def predictModelmatrix_ravexe(window_size,outfol0,param,dat_category,signaldats):
    outfol=addfol(outfol0,"matrix")
    outfol=addfol(outfol,dat_category)
    #dat_category = rest/task (default)
    
    result_record=[]
    rec_fn=os.path.join(outfol0,"result_"+dat_category+".csv")
    num_test=param.num_test#number of files to test

    for i, sdat in enumerate(signaldats):
        if num_test==-1 or i< num_test:
            sig0=sdat[0]
            datname0=sdat[2]#file name and path
            #data contents of default data (rest/task, task names etc)
            datname=getdatanames4defaultdat(datname0)
            f_sbn="file_"+str(i)
            output_f=addfol(outfol,f_sbn)
#            sig=preproc_normalizesignal(sig0) 
            sig=preproc_normalizesignal_runningaverage(sig0,window_size) 
            
            
            modelres=trainingmodel(sig,param, output_f,datname)
            pret=[f_sbn]
            pret=appendlist(pret,datname)
            pret=appendlist(pret,modelres)
            pret.append(datname0)
            result_record.append(pret)
            savefilenpcsv_str(result_record,rec_fn)


def trainingmodel(s0,param,  outfol,dname):
    ""
    name=liststr(dname)
    outfol_dat=addfol(outfol,"dat")
    rt=0.1#ratio for validation data 
    sig_trn, sig_val=splittrainingdat(s0, rt)
    #sig_tr, sig_ans=splitdat_trainingandanswer(s0,1)
    pmatfn=outfol+name+"_predmat.csv"
    if not os.path.exists(pmatfn):
        pmat=exetraining(param,  outfol_dat,name, sig_trn, sig_val)        
        savefilenpcsv(pmat,pmatfn)
    else:
        pmat=loadfilenpcsv(pmatfn)
    corval_tr, prv_trn = evalprediction(pmat, sig_trn)
    corval_val, prv_val = evalprediction(pmat, sig_val)
    ret=[corval_val,corval_tr]
    
    #save answer files
    savesignalfiles(sig_trn,prv_trn,sig_val,prv_val,outfol,name)
    return ret

def savesignalfiles(sig_trn,prv_trn,sig_val,prv_val,outfol,name):
    savefilenpcsv(sig_trn[0],outfol+name+"_trsig.csv")
    savefilenpcsv(sig_trn[1],outfol+name+"_transig.csv")
    savefilenpcsv(sig_val[0],outfol+name+"_vlsig.csv")
    savefilenpcsv(sig_val[1],outfol+name+"_vlansig.csv")
    savefilenpcsv(prv_trn,outfol+name+"_trprsig.csv")
    savefilenpcsv(prv_val,outfol+name+"_vlprsig.csv")
    


def loadtrainingmodel(output_f,param,  dname,dat_category):
    ""
    name=liststr(dname)
    #outfol_dat=addfol(outfol,"dat")
    pmatfn=output_f+name+"_predmat.csv"
    ret=[]
    if os.path.exists(pmatfn):
        pmat=loadfilenpcsv(pmatfn)
        sig_trn, prv_trn,sig_val,prv_val=loadsignalfiles(output_f,name)
        ret=[pmat,sig_trn, prv_trn,sig_val,prv_val]
    return ret

def loadsignalfiles(outfol,name):
    sig_trn0=loadfilenpcsv(outfol+name+"_trsig.csv")
    sig_trn1=loadfilenpcsv(outfol+name+"_transig.csv")
    sig_val0=loadfilenpcsv(outfol+name+"_vlsig.csv")
    sig_val1=loadfilenpcsv(outfol+name+"_vlansig.csv")
    prv_trn=loadfilenpcsv(outfol+name+"_trprsig.csv")
    prv_val=loadfilenpcsv(outfol+name+"_vlprsig.csv")
    sig_trn=[sig_trn0,sig_trn1]
    sig_val=[sig_val0,sig_val1]
    return sig_trn, prv_trn,sig_val,prv_val
    
    
    
    


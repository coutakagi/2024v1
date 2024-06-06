'''
Created on 2024/04/27

@author: coutakagi
'''
import os

from utlfiles import getfilelistinfol, addfol, getfilebasename, savefilenpcsv, savefilenpcsv_str, loadfilenpcsv, loadfilenpcsv_str
from fmriimg2sig import extractsignal, getConnectivitymatrix

#extract signal from fMRI image
def exeimg2sig(param):
    ret=[]
    fol_input0=param.fol_input#input image folder
    fol_input_dat=addfol(fol_input0,param.dataname)
    outfol0=param.fol_output#output folder
    outfol0=addfol(outfol0,"signal")
    dat_categories = param.subfol_img# rest/task
    for dat_category in dat_categories:
        fol_input=addfol(fol_input_dat,dat_category)
        outfol=addfol(outfol0,dat_category)
        pret=signaldata(fol_input,outfol,param)
        ret.append(pret)
    return ret
    
    

def signaldata(fol_input,outfol,param):
    outfiles=["_sig.csv","_fcmat.csv","_atlaslabel.csv"]
    #output file names #signal (main out), Functional connectivity (FC) matrix, brain atlas region label 
    ret=[]
    
    num_test=param.num_test
    filelist= getfilelistinfol(fol_input,"gz")
    for i, f in enumerate(filelist):
        if num_test==-1 or i< num_test:
            if i%10==0:
                if num_test>0:
                    print("load signal: {} / {}".format(len(ret), num_test))
                else:
                    print("load signal: {} / {}".format(len(ret), len(filelist)))
            outfn0, ouf0=getfilebasename(f, outfol)
            flg=0
            for fnsf in outfiles:
                fn=outfn0+fnsf
                if not os.path.exists(fn):
                    flg+=1
            if flg>0:#if file not exists 
                tsig, ainf=extractsignal(f, param)
                cmat=getConnectivitymatrix(tsig)
                saveresults([tsig,cmat, ainf],outfn0, outfiles)
                pret=[tsig,cmat, ouf0,ainf]
                ret.append(pret)
            else:
                #if exists load data from files 
                pret=loadsignaldatasets(outfn0,outfiles,ouf0)
                ret.append(pret)             
    return ret


def loadsignaldatasets(outfn0,outfiles,ouf0):
            fsig=outfn0+outfiles[0]
            fmat=outfn0+outfiles[1]
            finf=outfn0+outfiles[2]
            tsig=loadfilenpcsv(fsig)
            cmat=loadfilenpcsv(fmat)
            ainf=loadfilenpcsv_str(finf)
            pret=[tsig,cmat,ouf0,ainf]
            return pret


def saveresults(dats,outfn0, outfiles):
    #save results file in folder
    for i, (dat, outfile) in enumerate(zip(dats,outfiles)):
        if i<2:
            savefilenpcsv(dat, outfn0+outfile)
        else:
            savefilenpcsv_str(dat, outfn0+outfile)



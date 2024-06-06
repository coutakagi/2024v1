'''
Created on 2024/04/27

@author: coutakagi
'''
from param import paramSettings
from prepimg2sig import exeimg2sig
from predcmat import exeprediction, exeprediction_runningaverage


def exemainsequence(step):
    ""
    param=paramSettings()
    if step==0 or step==-1:
        image2signal(param)
    if step==1 or step==-1:
        predictConnectionMatrix(param)



def predictConnectionMatrix(param):
    predictConmatrix(param)
    #predcition with ruuning averaged signal data
    
    if param.exe_runningaverage==1:
        predictConmatrix_runningaverage(param)
    

def predictConmatrix(param):
    ""
    #predict connection matrix from signal 
    
    exeprediction(param)

def predictConmatrix_runningaverage(param):
    window_sizes=param.window_sizes
    exeprediction_runningaverage(param, window_sizes)
    
def image2signal(param):
    ""
    #extract signal from fMRI image
    
    sigdat=exeimg2sig(param)
    return sigdat
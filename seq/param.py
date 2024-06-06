'''
Created on 2024/04/27

@author: coutakagi
'''
class paramSettings(object):
    #data definition
    fol_input="./dat/input/"
    fol_output="./dat/res/"
    
    #default data set definition
    dataname="ds000224"#data set name
    #data example
    ##https://openneuro.org/datasets/ds000224

    subfol_img=["rest","task"]#main category
    
    num_test=-1#number of test files/images (if -1 = all) 
#    num_test=20#number of test files/images (if -1 = all) 

    
    #pre-process (images to signal)
    rois=100#number of ROIs of brain atlas (default=100)
    
    #model prediction
    training_repeat=3000
    eval_interval  =500
    
    #setting for running averaged signals
    exe_runningaverage=0# set 1 if execute running average
    window_sizes=[2,3,4,5]
    
    #statistics
    statistics_type=-1#all = -1, 0: stability, 1: summarize accuracy, 2: plot predictions, 3: correlation analysis  
    number_plot=1000#upper limit of number of plots
    
    
    def __init__(self):
        '''
        Constructor
        '''
        
'''
Created on 2024/04/27

@author: coutakagi
'''
import numpy as np
from nilearn.input_data import NiftiLabelsMasker
from nilearn.connectome import ConnectivityMeasure
from nilearn import image, datasets

#from nilearn.input_data import  NiftiMapsMasker

def extractsignal(f, param):
    masker, atlas_info=getatlsMasker(param)
    time_series = masker.fit_transform(f)
    return time_series, atlas_info



def getatlsMasker(param):
    # get atlas mask (Nilearn)
    rois=100#default number of ROIs
    if param.rois>0:
        rois=param.rois
#        atlas = datasets.fetch_atlas_schaefer_2018(n_rois=rois, yeo_networks=17)
    atlas = datasets.fetch_atlas_schaefer_2018(n_rois=rois, yeo_networks=7)
    atlas_filename = atlas.maps
    labels = atlas.labels
    atlas_info=getInfo_schaefer_2018(labels)
    masker = NiftiLabelsMasker(labels_img=atlas_filename, resampling_target='data', standardize=False)
    return masker,atlas_info

def getInfo_schaefer_2018(labels):
    #atlas label of schaefer 2018
    ret=[]
    for lb0 in labels:
        lb=str(lb0)
        lb=lb[2:(len(lb)-1)]
        netname=lb.split("_")[2]
        pret=[lb,netname]
        ret.append(pret)
    return ret


def getConnectivitymatrix(tsig):
    correlation_measure = ConnectivityMeasure(kind='correlation')
    correlation_matrix = correlation_measure.fit_transform([tsig])[0]
    # Mask out the major diagonal
    np.fill_diagonal(correlation_matrix, 0)    
    return correlation_matrix    
    

def getatlasmap(rois):
    atlas = datasets.fetch_atlas_schaefer_2018(n_rois=rois, yeo_networks=7)
    atlas_map = atlas.maps
    return atlas_map
    

def getatlasnetinf(rois):
    atlas = datasets.fetch_atlas_schaefer_2018(n_rois=rois, yeo_networks=7)
    atlas_filename = atlas.maps
    img0=image.load_img(atlas_filename)
    img=image.get_data(atlas_filename)
    img=np.array(img)        
    labels = atlas.labels
    atlas_info=getInfo_schaefer_2018(labels)
    return img,img0,atlas_info


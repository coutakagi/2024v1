'''
Created on 2024/04/28

@author: coutakagi
'''
import tensorflow as tf
import numpy as np
import os
from evaluatemodelresult import evalprediction_plot
from utldat import settextfromlist


def exetraining(param,  outfol_dat,name, sig_trn, sig_val):
    #trainingTFv2 
    ""
    step=param.training_repeat
    eval_interval=param.eval_interval
    inpt,_=getdatasetTF(sig_trn)

    x=(sig_trn[0].T).shape[0]
    cmat0=getrandmatini(x,x)
    
    dta=tf.Variable(cmat0)
    dta=tf.cast(dta,tf.double)
    
    optimizer = tf.keras.optimizers.Adam()
    
    for i in range(step+1):
        with tf.GradientTape() as tape:
            loss=getLossv2([dta, inpt])
        grads = tape.gradient(loss, [dta])
        optimizer.apply_gradients(zip(grads,[dta])) 
        if i%eval_interval==0 or i==step:
            pret=[name, i]
            fn_cor_tr=os.path.join(outfol_dat,name+"_"+str(i)+"_tr.png")
#            evl_tr,_=evalprediction(dta.numpy(), sig_trn)
            evl_tr,_=evalprediction_plot(fn_cor_tr,dta.numpy(), sig_trn)
            fn_cor_vl=os.path.join(outfol_dat,name+"_"+str(i)+"_tr.png")
            evl_vl,_=evalprediction_plot(fn_cor_vl,dta.numpy(), sig_val)
            
            pret.append(evl_vl)
            pret.append(evl_tr)
            mean_loss=np.mean(loss.numpy())
            pret.append(mean_loss)
            s=settextfromlist(pret)
            print(s)
    mean_loss=np.mean(loss.numpy())
    return dta.numpy()

def getdatasetTF(sig_trn):
    st=sig_trn[0].T
    ans=sig_trn[1].T
    inpt=tf.Variable(st)    
    inpt=tf.cast(inpt,tf.double)
    return inpt, ans


def getLossv2(dat):
    dta=dat[0]
    inpt=dat[1]
#    inpt=divmean(inpt)
    inpt=divnorm(inpt)
    
    outp=tf.matmul(dta, inpt)
#    outp=divmean(outp)
    outp=divnorm(outp)
    
    loss1=tf.multiply(inpt, outp)
    loss2=tf.multiply(outp, outp)
    loss= loss2-loss1
    loss=tf.reduce_mean(loss,axis=1)
    return loss
def divnorm(pred):
#    pm=tf.reduce_mean(pred)
    pm=tf.math.reduce_std(pred)
    
    pm=tf.abs(pm)
    if not tf.equal(pm,0):
        pred=tf.divide(pred,pm)
    return pred    


def getrandmatini(x,y):
    ret=np.random.rand(x*y)
    ret=np.reshape(ret, (x,y))
    return ret


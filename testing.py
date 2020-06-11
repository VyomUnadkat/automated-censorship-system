#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 18 11:28:24 2018

@author: vyomunadkat
"""
import numpy as np
from scipy import spatial

    
    
#calculating the difference between the f.v.
def mse(imageA, imageB):
    err = np.sum((imageA.astype("float") - imageB.astype("float")) ** 2)
    err /= float(imageA.shape[0] * imageA.shape[1])
    return err


def similar(imageA, imageB):
    m = 1 - mse(imageA, imageB)
    s = 1 - spatial.distance.cosine(imageA, imageB)
    b = spatial.distance.euclidean(imageA, imageB)
    print(m)
    print(s)
    if (s>=0.97 and m>=0.99):
        return True
    else:
        return False



data = np.load('bohemain_360.npy')
data1 = np.load('bohemain_720_60.npy')
data2 = np.load('bohemain_720_60_blur.npy')


mse(data, data1)
mse(data, data2)
    
reference_list_fr = pd.DataFrame(
                              {'video': files_fr,
                              'duration': duration_fr,
                              'feature_vector' : fv_fr,
                              't/f' : true_or_false
                              })
    
# JUST TESTING

#euclidian
import scipy.stats as stats
a= reference_list_cll.iloc[1]['feature_vector']
b= reference_list_fr.iloc[8]['feature_vector']

dist = np.linalg.norm(a-b)
print(dist)


#chi squared

def chiSquared(p,q):
    return 0.5*np.sum((p-q)**2/(p+q+1e-6))



a= reference_list_cll.iloc[0]['feature_vector']
b= reference_list_fr.iloc[3]['feature_vector']


print(chiSquared(a,b))
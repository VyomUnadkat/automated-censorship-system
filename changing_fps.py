#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul  4 15:31:29 2018

@author: vyomunadkat
"""

#importing the libraries
import matplotlib.pyplot as plt
import numpy as np
import cv2
import time
from skimage.measure import compare_ssim as ssim
from os import listdir
from os.path import isfile, join
import numpy
import cv2
import os
import natsort
import pandas as pd
import imutils
from PIL import Image
import PIL
from PIL import Image
import subprocess

#converting frame to 60 fps
source = 'fr.mp4'
destination = './fr/fr.mp4'
fps = '60'

d='ffmpeg -y -i '+source+' -r '+fps+' -s 1280x720 -vcodec mpeg4 -b:v 3M -strict -2 -movflags faststart '+ destination
subprocess.call(d, shell=True)



cap = cv2.VideoCapture('fr.mp4')
print(cap.get(cv2.CAP_PROP_FPS))

cap1 = cv2.VideoCapture('./fr/fr.mp4')
print(cap1.get(cv2.CAP_PROP_FPS))


#converting clip to 60 fps
source = 'cll.mp4'
destination = './cll/cll.mp4'
fps = '60'

d='ffmpeg -y -i '+source+' -r '+fps+' -s 1280x720 -vcodec mpeg4 -b:v 3M -strict -2 -movflags faststart '+ destination
subprocess.call(d, shell=True)


cap2 = cv2.VideoCapture('cll.mp4')
print(cap2.get(cv2.CAP_PROP_FPS))

cap3 = cv2.VideoCapture('./cll/cll.mp4')
print(cap3.get(cv2.CAP_PROP_FPS))


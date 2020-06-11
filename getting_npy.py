import csv
import pandas as pd
import numpy as np
import natsort
import os
import moviepy
from moviepy.editor import VideoFileClip
from skimage.measure import compare_ssim as ssim
from scipy import spatial
import subprocess
from PIL import Image


#USE this command in TERMINAL TO REMOVE .DS_Store file
'''
import glob, os

i=0
for root, dirs, files in os.walk('/'):
    for file in files:
        if file.endswith('.DS_Store'):
            path = os.path.join(root, file)

            print("Deleting: %s" % (path))

            if os.remove(path):
                print("Unable to delete!")
            else:
                print("Deleted...")
                i += 1

print("Files Deleted: %d" % (i))
'''




#e = 'sudo find / -name ".DS_Store" -depth -exec rm {} \;'
#subprocess.call(e, shell=True)


fr = []
duration_fr = []
fv_fr = []

for path, dirs, files_fr in os.walk("./fr_npy/visual/"):
    files_fr = natsort.natsorted(files_fr)

for path, dirs, files_fr_vid in os.walk("./fr/fr/Shots/"):
    files_fr_vid = natsort.natsorted(files_fr_vid)
    print(files_fr_vid)
    


len_fr = len(files_fr)
print(len_fr)


true_or_false = [False] * (len_fr)

for i in range(1,len_fr+1):
    clip = VideoFileClip('./fr/fr/Shots/fr_%d.mp4' % i)
    duration_fr.append(clip.duration)
    data = np.load('./fr_npy/visual/fr_%d.npy' % i)
    fv_fr.append(data)

print(duration_fr)
print(len(duration_fr))
    
start_ts_fr = np.load('start_fr.npy')
end_ts_fr = np.load('end_fr.npy')
start_ts_fr = start_ts_fr[1:]
end_ts_fr = end_ts_fr[1:]
    
reference_list_fr = pd.DataFrame(
                              {'video': files_fr_vid,
                              'duration': duration_fr,
                              'feature_vector' : fv_fr,
                              'starting_ts' : start_ts_fr,
                              'ending_ts' : end_ts_fr
                              })
    
    

    
#creating reference list for cll

cll = []
duration_cll = []
fv_cll = []


for path, dirs, files_cll in os.walk("./cll_npy/visual/"):
    files_cll = natsort.natsorted(files_cll)


len_cll = len(files_cll)
print(len_cll)


for i in range(1,len_cll+1):
    clip = VideoFileClip('./cll/cll/Shots/cll_%d.mp4' % i)
    duration_cll.append(clip.duration)
    data = np.load('./cll_npy/visual/cll_%d.npy' % i)
    fv_cll.append(data)

print(duration_cll)
print(len(duration_cll))

start_ts_cll = np.load('start_cll.npy')
end_ts_cll = np.load('end_cll.npy')
start_ts_cll = start_ts_cll[1:]
end_ts_cll = end_ts_cll[1:]
    
    
    
reference_list_cll = pd.DataFrame(
                              {'video': files_cll,
                              'duration': duration_cll,
                              'feature_vector' : fv_cll,
                              'starting_ts' : start_ts_cll,
                              'ending_ts' : end_ts_cll
                              })
    
    
    
#calculating the difference between the f.v.
def mse(imageA, imageB):
    err = np.sum((imageA.astype("float") - imageB.astype("float")) ** 2)
    err /= float(imageA.shape[0] * imageA.shape[1])
    return err


def similar(imageA, imageB):
    m = mse(imageA, imageB)
    s = 1 - spatial.distance.cosine(imageA, imageB)
    b = spatial.distance.euclidean(imageA, imageB)
    print(m)
    print(s)
    if (s>=0.97 and m<=50):
        return True
    else:
        return False
    
a = fv_cll[11]
b = fv_fr[19]
a=a.reshape((1,2048))
b=b.reshape((1,2048))
if not b.any():
  print("List is empty")
  b = [0] * 2048
  b = np.reshape(b,(1,2048))
if not a.any():
  print("List is empty")
  a = [0] * 2048
  a = np.reshape(a,(1,2048))
print(mse(a,b))
similar(a,b)

def find():
    i = 0
    j = 0
    while(i< len_cll):
        image1 = reference_list_cll.iloc[i]['feature_vector']
        image1 = image1.reshape((1,2048))
        print(image1.shape)
        print(image1)
        while(j<len_fr):
            image2 = reference_list_fr.iloc[i+j]['feature_vector']
            image2 = image2.reshape((1,2048))
            print(image2.shape)
            print(image2)
            isSimilar = similar(image1, image2)
            print(isSimilar)
            print("Comparing video %d in clip to image %d in frame" %(i,i+j))
            if isSimilar == True:
                true_or_false[i+j] = True
                break
            j = j + 1
        i = i + 1
        
find()




    
reference_list_fr = pd.DataFrame(
                              {'video': files_fr_vid,
                              'duration': duration_fr,
                              'feature_vector' : fv_fr,
                              't/f' : true_or_false,
                              'starting_ts' : start_ts_fr,
                              'ending_ts' : end_ts_fr
                              })
    
'''
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
'''

# REMOVING THE FILES THAT ARE NOT PRESENT
'''
import os
filenn = 'test1.npy'
myfile="cll/cll/Shots/"+filenn

## If file exists, delete it ##
if os.path.isfile(myfile):
    #os.remove(myfile)
else:    ## Show an error ##
    print("Error: %s file not found" % myfile)
'''


for i in range(0,len_fr):
    torf = reference_list_fr.iloc[i]['t/f']
    #print(torf)
    if torf == False:
        #print(i)
        #print('shit its false')
        filenn = reference_list_fr.iloc[i]['video']
        print(filenn)
        myfile="fr/fr/Shots/"+filenn
        print(myfile)
        ## If file exists, delete it ##
        if os.path.isfile(myfile):
            #os.remove(myfile)
            print('file_removed')
        else:    ## Show an error ##
            print("Error: %s file not found" % myfile)

#combining videos
            '''
from moviepy.editor import *

for path, dirs, clips in os.walk("./fr/fr/Shots/"):
    clips = natsort.natsorted(clips)
    


fade_duration = 1 # 1-second fade-in for each clip
clips = [clip.crossfadein(fade_duration) for clip in clips]

final_clip = concatenate_videoclips(clips, padding = -fade_duration)

# You can write any format, in any quality.
final_clip.write_videofile("final.mp4", bitrate="5000k")




'''

starting_scenes =[]
ending_scenes = []

#getting the starting scenes
i=0


if reference_list_fr.loc[0]['t/f'] == False:
    starting_scenes.append(reference_list_fr.loc[0]['starting_ts'])

lenn = len(reference_list_fr)
for i in range(lenn):
    if (reference_list_fr.loc[i]['t/f'] == False and (reference_list_fr.loc[i-1]['t/f'] == True)):
        starting_scenes.append(reference_list_fr.loc[i]['starting_ts'])

    
j=0

lenn = len(reference_list_fr)
for j in range(lenn):
    if (reference_list_fr.iloc[j]['t/f'] == True and (reference_list_fr.iloc[j-1]['t/f'] == False)):
        ending_scenes.append(reference_list_fr.iloc[j-1]['ending_ts'])
    

if reference_list_fr.loc[reference_list_fr.index[-1]]['t/f'] == False:
    ending_scenes.append(reference_list_fr.loc[j]['ending_ts'])  
'''

#ffmpeg -i video.mp4 -af "volume=enable='between(t,5,10)':volume=0, volume=enable='between(t,15,20)':volume=0" ...


e="ffmpeg -i coldplay.wav -af \"volume=enable='between(t,5,10)':volume=0, volume=enable='between(t,33,36)':volume=0\" outputt2.wav"
subprocess.call(e, shell=True)

#ffmpeg -i coldplay.wav -af "volume=enable='between(t,5,10)':volume=0, volume=enable='between(t,33,36)':volume=0" outputt.wav



input_file = "coldplay.wav"

e = 'ffmpeg -i' +input_file+'-af "vulome=enable=\'between(t,5,10)\':volume=0"'

print(e)
'''



def get_sec(time_str):
    h, m, s = time_str.split(':')
    print(h)
    print(m)
    print(s)
    return float(h) * 3600 + float(m) * 60 + float(s) 



inputfile = 'coldplay2.wav'
first = 'ffmpeg -i '
second = '%s '%inputfile
third = '-af \"'
fourth = 'volume=enable=\'between'
fifth = '(t,%f,%f)\':volume=0'%(get_sec(starting_scenes[0]),get_sec(ending_scenes[0]))
final_command = first+second+third+fourth+fifth



first_half = first+second+third+fourth+fifth

for i in range(1,len(starting_scenes)):
    a=get_sec(starting_scenes[i])
    b=get_sec(ending_scenes[i])
    c=', volume=enable=\'between'
    first_half = first_half+c+'(t,%f,%f)\':volume=0'%(a,b)

first_half = first_half + '" finalout.wav'

subprocess.call(first_half, shell=True)


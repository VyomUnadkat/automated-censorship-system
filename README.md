# deep-features-video

Script to extract CNN features from video frames using a Keras pre-trained VGG-19 model.





######NOTEEEE

get tensorflow version 1.4.0 and keras version 2.0.8
otherwise it doesn't work


'cll' is the short clip we need to fing from the long movie 'fr'.
we divide both the videos based on camera cuts.
the concept of extracting features employed for video captioning have been used to compare each camera cut's features in both the video.
the scenes that were similar were mapped to their exact timestamp and we would get our results.

my task was to also map the audio and mute the part that was similar in both the videos, so as an example I have muted the part that was common in the 'coldplay.wav'

sequence of files to be executed.
1. changing_fps.py

this is done to set the fps and resolution of both the videos to be the same 60 fps and 720p

2. video_to_shots_cll.py
3. video_to_shots_fr.py

we use pyscenedetect to accomplish this.

4. extract_features_cll.py
5. extract_features_fr.py
to extract the features of all the shots in both fr and cll as a numpy file(.npy)

6. getting_npy.py
script to compare the features of both videos as per camera cuts and get the timestamp of the similar portion.
This would also mute the audio between those timestamps in the coldplay.wav file.



You can place the fr.mp4 and cll.mp4 in the same folder as the scrips and rest would be taken care of.

Thank you.

 

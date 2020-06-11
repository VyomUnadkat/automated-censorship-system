# importing major libraries
import os
from os import listdir, mkdir, rename
from os.path import join, isfile, splitext, basename
from shutil import rmtree, move
from PySceneDetect.scenedetect.manager import SceneManager
from PySceneDetect.scenedetect import timecodes
from PySceneDetect.scenedetect import detectors
from PySceneDetect.scenedetect import cli
from PySceneDetect.scenedetect.__init__ import detect_scenes_file
import glob
import numpy as np
import pickle

starting_ts = []
ending_ts = []

# assigning variables
ARGUMENTS = "-i %s -d content -t %d -q"
threshold = 25
start_time = '00:00:00.000'
end_time = ''


# function for generating video to shots
def video_to_shot_timestamp(data_folder_path, video_path):
    # making the folder structure
    video_name = splitext(basename(video_path))[0]
    try:
        mkdir(join(data_folder_path, video_name))
    except OSError:
        rmtree(join(data_folder_path, video_name))
        mkdir(join(data_folder_path, video_name))
        pass

    # moving the video into the folder
    #move(join(data_folder_path, video_path), join(data_folder_path, video_name, video_path))

    # creating a shots folder
    mkdir(join(data_folder_path, video_name, 'Shots'))

    # input video path
    input_video = join(data_folder_path, video_name, video_path)

    # setting up arguments for pyscene library
    args = ARGUMENTS % (join(data_folder_path, video_name, video_path), threshold)
    scene_detectors = detectors.get_available()
    timecode_formats = timecodes.get_available()
    parser = cli.get_cli_parser(scene_detectors.keys(), timecode_formats.keys())
    args = parser.parse_args(args.split())
    smgr = SceneManager(args, scene_detectors)

    # generating shot-break time stamp
    try:
        video_fps, frames_read, frames_processed = detect_scenes_file(path=args.input.name, scene_manager=smgr)
        end_time = timecodes.get_string(frames_processed * 1000 / float(video_fps))
    except ValueError as error_description:
        print('error in reading video files - corrupted video file! %s',
              error_description)
        raise ValueError
    scene_lit_milliseconds = [(1000.0 * x) / float(video_fps) for x in smgr.scene_list]
    scene_list_timecodes = [timecodes.get_string(x) for x in scene_lit_milliseconds]
    video_ts = [start_time]
    [video_ts.append(x) for x in scene_list_timecodes]
    video_ts.append(str(end_time))
    print(video_ts)


    [video_to_clip(input_video, video_ts[i], video_ts[i + 1],
                   join(data_folder_path, video_name,"Shots", video_name + '_' + str(i) + '.mp4')) for i in
     range(len(video_ts) - 1)]

    return video_ts





def video_to_clip(original_video, t1, t2, destination_file_name):
    starting_ts.append(str(t1))
    ending_ts.append(str(t2))
    print('ffmpeg -loglevel quiet -i ' + original_video + ' -ss ' + str(t1) + ' -to ' + str(t2) + ' -strict -2 '+' ' + destination_file_name + ' -y')
    os.system('ffmpeg -loglevel quiet -i ' + original_video + ' -ss ' + str(t1) + ' -to ' + str(t2) +' -strict -2 '+ ' ' + destination_file_name + ' -y')


# calling main function
if __name__ == '__main__':
    current_dir_path = os.path.dirname(os.path.realpath('/Users/vyomunadkat/Desktop/fv_new_final/'))
    data_folder_path = os.path.join(current_dir_path, '/Users/vyomunadkat/Desktop/fv_new_final/cll/')
    if os.path.exists(data_folder_path):
        print('Data folder found - proceeding forward')
    else:
        print('Data folder not found')

    # removing all spaces from filenames
    # for file in listdir(data_folder_path):			
    #     rename(join(data_folder_path, file), join(data_folder_path, file.replace(' ', '')))

    # list_of_videos = [file for file in listdir(data_folder_path) if
    #                   isfile(join(data_folder_path, file))]

    list_of_videos = []
    for file in glob.glob(data_folder_path+'/*'):
    	list_of_videos.append(file)
    print(list_of_videos)

    status = [video_to_shot_timestamp(data_folder_path, file) for file in list_of_videos]
    print(starting_ts)
    print(ending_ts)


feat_filepath = os.path.join( 'start_cll.npy')

with open(feat_filepath, 'wb') as f:
    np.save(f, starting_ts)

feat_filepath = os.path.join( 'end_cll.npy')

with open(feat_filepath, 'wb') as f:
    np.save(f, ending_ts)

ss = np.load('start_cll.npy')
ee = np.load('end_cll.npy')

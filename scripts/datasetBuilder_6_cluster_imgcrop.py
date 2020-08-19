#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 22 20:06:29 2020
We use the output files from pyannote video tools 
and detect the faces using FaceClustering.
We assume the speakers shows more frequently than others.
So the most frequently appeared label will be seen as the speaker.
Then we extract frames and cropped them out 
based on the time and box of the speaker from the track.txt file.
@author: loewi
"""

import os
from pyannote.video.face.clustering import FaceClustering
import cv2
from pyannote.video import Video
import random
random.seed(2020)
import pandas as pd
import numpy as np  
import subprocess

NAMES = ['t', 'track', 'left', 'top', 'right', 'bottom', 'status']
DTYPE = {'left': np.float32, 'top': np.float32,
          'right': np.float32, 'bottom': np.float32}

ROOT_DIR = './merged_snippets'
SHELL_SCRIPT = "./cut_frames.sh"


def face_clustering(embedding_file):
    """
    Use pyannote to cluster face

    Parameters
    ----------
    embedding_file : txt
        DESCRIPTION.

    Returns
    -------
    result : pyannote.core.annotation.Annotation
        DESCRIPTION.

    """
    clustering = FaceClustering(threshold=0.6)
    face_tracks, embeddings = clustering.model.preprocess(embedding_file)
    result = clustering(face_tracks, features=embeddings)
    print(result)
    return result

def isvalid(file_name):
    """
    Check if the video have 3 txt files and 1 json file
    e.g. xxx.mp4 should have files as follows:
    xxx.embedding.txt
    xxx.landmarks.txt
    xxx.shots.json
    xxx.track.txt

    Parameters
    ----------
    file_name : txt
        DESCRIPTION.

    Returns
    -------
    boolean
        DESCRIPTION.

    """
    return os.path.isfile(f'{ROOT_DIR}/{file_name}.mp4') and \
           os.path.isfile(f'{ROOT_DIR}/{file_name}.embedding.txt') and \
           os.path.isfile(f'{ROOT_DIR}/{file_name}.landmarks.txt') and \
           os.path.isfile(f'{ROOT_DIR}/{file_name}.shots.json') and \
           os.path.isfile(f'{ROOT_DIR}/{file_name}.track.txt')

def get_track(embedding_file):
    """
    Find the track. 

    Parameters
    ----------
    embedding_file : txt
        DESCRIPTION.

    Returns
    -------
    track: pandas.core.series.Series
        if there is only one label, return track,
        else we should ingnore this file.

    """
    result = face_clustering(embedding_file)
    result_json = result.for_json()
    df = pd.DataFrame(result_json['content'])
    lbl = df.label.mode()  # select the most frequent value(s)
    # e.g. if the label is 7, we should go back to the df and pick out all the track that labeled 7
    if len(lbl) == 1:
        track = df[df['label'] == int(lbl)]['track']
        return track
    

def choose_track(tracking_file, track):
    """
    Select the tracks that has the right label

    Parameters
    ----------
    tracking_file : txt
        DESCRIPTION.
    track : pandas.core.series.Series
        result from get_track() function

    Returns
    -------
    df_one : pandas.core.frame.DataFrame
        e.g.
        t  track   left    top  right  bottom            status
    1.502      1  0.662  0.171  0.777   0.376  forward+backward
    7.908      2  0.381  0.160  0.550   0.459  forward+backward
    ...
    
    """
    tracking = pd.read_table(tracking_file, delim_whitespace=True, header=None,
                              names=NAMES, dtype=DTYPE)
    tracking = tracking.sort_values('t')
    # pick out only those selected tracks
    df_t = tracking[tracking['track'].isin(track) ]
    # randomly selected one row for each group ('track')
    print("df_t", df_t)
    df_one = df_t.groupby('track').apply(pd.DataFrame.sample, n=1, random_state=2020).reset_index(drop=True)
    print('speaker identified!')
    return df_one


def get_face_box(img, video, row, hyper_r=0.2):
    """
    Get the face box according to the img size and video size

    Parameters
    ----------
    img :  numpy.ndarray
        DESCRIPTION.
    video : pyannote.video.video.Video
        DESCRIPTION.
    row : pandas.core.series.Series
        DESCRIPTION.
    hyper_r : float, optional
        DESCRIPTION. The default is 0.2.

    Returns
    -------
    left : int
        DESCRIPTION.
    right : int
        DESCRIPTION.
    top : int
        DESCRIPTION.
    bottom : int
        DESCRIPTION.

    """
    
    frame_width, _, _ = img.shape
    height=frame_width
    video_width, video_height = video.frame_size
    ratio = height / video_height
    width = int(ratio * video_width)
    video.frame_size = (width, height)  
    
    left = int(row['left'] * width)
    right = int(row['right'] * width)
    top = int(row['top'] * height)
    bottom = int(row['bottom'] * height)
    print('original face box coordinates: ', left, right, top, bottom)
    
    if hyper_r:
        dx = (right - left) * hyper_r
        dy = (bottom - top) * hyper_r
        left = int(left - dx)
        right = int(right + dx)
        top = int(top - dy)
        bottom = int(bottom + dy)
        print('enlarged face box coordinates: ', left, right, top, bottom)

    return left, right, top, bottom


def extract_frame(time, input_video, output_pic):
    """
    Run the command with subprocess

    Parameters
    ----------
    time : float
        DESCRIPTION.
    input_video : string
        DESCRIPTION.
    output_pic : string
        DESCRIPTION.

    Returns
    -------
    None''

    """
    # $time -> $1; $input_video -> $2; $output_pic -> $3
    # ffmpeg -ss $1 -i $2 -vframes 1 -q:v 2 $3
    # caveate: chmod +x cut_frames.sh
    subprocess.check_call([SHELL_SCRIPT, str(time), input_video, output_pic], shell=False)
    

with open(f'{ROOT_DIR}/merged_files.txt', 'r') as f:
    merged_files_list = f.read().splitlines()

merged_files_name_list = sorted([file.split('/')[-1][:-4]for file in merged_files_list])

seen = []
for file_name in merged_files_name_list[0]:
    if not isvalid(file_name): continue # check the video file and others
    print(f'{file_name} processing...')
    # save all the frames into the directory
    embedding_file = f'{ROOT_DIR}/{file_name}.embedding.txt'
    tracking_file = f'{ROOT_DIR}/{file_name}.track.txt'
    input_video = f'{ROOT_DIR}/{file_name}.mp4'
    output_picdir = f'{ROOT_DIR}/{file_name}_frames'
    output_cropped_picdir = f'{ROOT_DIR}/cropped_frames/{file_name}_cropped_frames'
    
    if not os.path.exists(output_picdir): 
        os.makedirs(output_picdir) 
    if not os.path.exists(output_cropped_picdir): 
        os.makedirs(output_cropped_picdir) 
    else:
        print(f'{file_name}_cropped_frames directory already exist')
        seen.append(file_name)
        continue
    
    track = get_track(embedding_file)
    if track is None: continue
    
    # e.g. './snippets/2018-03-30_0100_US_CNN_Anderson_Cooper_360_merged_Christine_Quinn.track.txt'
    df_one = choose_track(tracking_file, track)
    
    # cut
    video = Video(input_video)

    for i, row in df_one.iterrows():
        
        print('frames extracting...')
        output_pic = f'{output_picdir}/{i}_{file_name}.jpg'
        output_cropped_pic = f'{output_cropped_picdir}/{i}_{file_name}.jpg'
        if os.path.exists(output_pic) :continue
        
        time = row['t']
        print(f'extracting the frame at {time}...')
        extract_frame(time, input_video, output_pic)
        print(f'{output_pic} is done!')
        
        print('frames cropping...')
        img = cv2.imread(output_pic)
        left, right, top, bottom = get_face_box(img, video, row, hyper_r=0.2)
        crop_img = img[top:bottom, left:right]
        cv2.imwrite(output_cropped_pic, crop_img)
        print(f'{output_cropped_pic} is done!')

with open(f'{ROOT_DIR}/log', 'w') as f:
    for s in seen:
        f.write(f'{s}\n')

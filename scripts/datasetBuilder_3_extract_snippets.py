#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 18 01:25:40 2020

pip install ffmpeg-python


@author: loewi
"""
import ffmpeg
import json
import os
import pandas as pd
import sys

def trim(input_path, output_path, start=20, end=22):
    """
    Trim the video using the ffmpeg-python.
    :param input_path: string
    :param output_path: string
    :param start: seconds
    :param end: seconds
    :return: video snippet (output_path)
    """
    try:
        print(f'input path: {input_path}')
        if not os.path.isfile(input_path):
            print("cannot find the input file")
            return "unfinished"
        
        
        input_stream = ffmpeg.input(input_path)
    
        vid = (
            input_stream.video
            .trim(start=start, end=end)
            .setpts('PTS-STARTPTS')
        )
        aud = (
            input_stream.audio
            .filter_('atrim', start=start, end=end)
            .filter_('asetpts', 'PTS-STARTPTS')
        )
    
        joined = ffmpeg.concat(vid, aud, v=1, a=1).node
        output = ffmpeg.output(joined[0], joined[1], output_path)
        output.run()
        print(f"snippet created in {output_path}")
        return "finished"
    except:
        print(f"snippet failed in {output_path}")
        return "unfinished"
    
    
def create_input_path(ori_filename):
    """
    path should be absolute 
    from "2018-05-25_1700_US_CNN_Wolf"
    to "/mnt/rds/redhen/gallina/tv/2018/2018-05/2018-05-25/2018-05-25_1700_US_CNN_Wolf.mp4"
    :param filename: string
    :return: string
    """
    ymd = ori_filename[:10]
    ym = ymd[:7]
    return f"/mnt/rds/redhen/gallina/tv/2018/{ym}/{ymd}/{ori_filename}.mp4"


def trim_video(lean_corpus_file):
    """
    Cut the video by a start time (seconds) and an end time (seconds).

    :param lean_corpus_file: string, path of the file
    :return: dump the snippets of the video
    """
    with open(lean_corpus_file) as f:
        data = json.load(f)

    for file_name, persons_dict in data.items():
        input_path = create_input_path(file_name)
        for person, info_dict in persons_dict.items():
            gender = info_dict['gender']
            age = info_dict['age']
            time_list = info_dict['time']
            for start_time, end_time in time_list:

                output_path = f'./snippets/{file_name}_{start_time}-{end_time}_{person}.mp4'        
                if os.path.exists(output_path):
                    continue
                csv_file = "./output/snippets_info_with_age_gender.csv"
                if os.path.exists(csv_file):
                    snippet_df = pd.read_csv(csv_file)
                    
                    if file_name not in snippet_df['file_name']:
                        result = trim(input_path, output_path, start=start_time, end=end_time)
                        df = pd.DataFrame({'file_name': [file_name],
                                           'input_path': [input_path],
                                           'output_path': [output_path],
                                           'start_time': [start_time],
                                           'end_time': [end_time],
                                           'person' : [person],
                                           'gender' : [gender],
                                           'age': [age],
                                           'result': [result]
                                           })
                        df.to_csv(csv_file,  mode='a', header=False)
                else:

                    result = trim(input_path, output_path, start=start_time, end=end_time)
                    
                    df = pd.DataFrame({'file_name': [file_name],
                                       'input_path': [input_path],
                                       'output_path': [output_path],
                                       'start_time': [start_time],
                                       'end_time': [end_time],
                                       'person' : [person],
                                       'gender' : [gender],
                                       'age': [age],
                                       'result': [result]
                                       })
                    
                    df.to_csv(csv_file)



if __name__ == "__main__":

    # corpus_path = "./lean_corpus_2018.json"
    # trim_video(corpus_path)
    args = sys.argv
    if len(args) != 2:
        raise Exception("not valid ")
    else:
        corpus_path = args[1]
        trim_video(corpus_path)
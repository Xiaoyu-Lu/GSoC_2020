#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  6 21:29:40 2020

@author: loewi
concat the snippets that has the same speaker and same age 
"""
import pandas as pd
import ffmpeg
import os

def concate(files, output_file):
    """
    Concat the video using the ffmpeg-python.
    """
    (
        ffmpeg
        .input(files, format='concat', safe=0)
        .output(output_file, c='copy')
        .run()
    )
    if not os.path.isfile(output_file):
        print("cannot find the output file")
        return "failed"
    return "concated"

csv_file = './output/snippets_info_with_age_gender.csv'
with open(csv_file, 'r'):
    df = pd.read_csv(csv_file)
gp = df.groupby(by=['person','gender','age'])

output_filelist = []
for k, v in gp.groups.items():
    print(k, v.values )
    # ('Aaron_David_Miller', 68) [1542 1543 1544 1545]
    rows = df[df.index.isin(v.values)]
    paths = rows['output_path']
    # e.g. output path: ./snippets/2018-05-22_2000_US_CNN_The_Lead_With_Jake_Tapper_572.4-588.66_Sam_Clovis.mp4
    print(rows)
    
    name, gender, age = k
    with open('./mylist.txt', 'w') as f:
        for path in paths:
            f.write(f'file \'{path}\'\n')

    files = './mylist.txt' # temporary file as ffmpeg input
    output_file = f'./merged_snippets/{name}-{gender}-{age}.mp4'
    if not os.path.isfile(output_file):
        concate(files, output_file)
        output_filelist.append(f'./{name}-{gender}-{age}.mp4')
     
with open('./merged_snippets/merged_files.txt', 'w') as f:
    for file in output_filelist:
        f.write(f'{file}\n')
    


#!/bin/bash
# input_video='./snippets/s/2018-03-30_0100_US_CNN_Anderson_Cooper_360_merged_Christine_Quinn.mp4'
# ffmpeg -ss 3.470 -i $input_video -vframes 1 -q:v 2 output.jpg
# ffmpeg -ss 8.342 -i $input_video -vframes 1 -q:v 2 output1.jpg
# input_video='xxx.mp4'
ffmpeg -ss $1 -i $2 -vframes 1 -q:v 2 $3
#!/bin/bash
input_path="./pred/videos/2018-02-09_0100_US_CNN_Anderson_Cooper_360_3224.7-3244.7_Amanda_Carpenter.mp4"
length=${#input_path}
endindex=$(expr $length - 4)
output_path="${input_path:0:$endindex}_out.avi"
python3 ./pred/pred.py --video $input_path --output "${output_path}"
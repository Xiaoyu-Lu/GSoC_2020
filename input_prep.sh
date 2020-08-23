#!/bin/bash
mkdir -p output
# get gentle paths in 2018 directory
year=2018
directory="/mnt/rds/redhen/gallina/tv/${year}"
gentlepath="./output/gentle_paths.txt"
find $directory -type f -name "*.gentleoutput.json" > $gentlepath

# transform tpt files into json
tpt_json="./output/corpus_${year}.json"
python3 ./scripts/datasetBuilder_0_gentle_and_tpt.py gentlepath $tpt_json

# build speaker database, output = './output/speaker_db_{year}.json'
python3 ./scripts/datasetBuilder_1_speaker_db.py $tpt_json 

# concatenate new database with the original one using jq
# Linux：jq 1.5 is in the official Debian and Ubuntu repositories. Install using sudo apt-get install jq
# OS X：Use Homebrew to install jq 1.6 with brew install jq.
archive_path="./output/archive"
db_path=".${archive_path}/speaker_db.json"
new_db_path="./output/speaker_db.json"
jq -s '.[0] * .[1]' $tpt_json $db_path > $new_db_path
# compare the new with old
diff <(jq -S . $db_path) <(jq -S . $new_db_path)
# overwrite the old with the new if the old one exists
mv -i $new_db_path $archive_path

# insert the speakers' info into the tpt_json file
lean_path="./output/lean_corpus_${year}.json"
python3 ./scripts/datasetBuilder_2_lean.py $tpt_json $lean_path

# extract video snippets base on the time intervals in the lean_path file
# need to install ffmpeg-python with pip install ffmpeg-python
# the script also yields an csv file "./output/snippets_info_with_age_gender.csv"
python3 ./scripts/datasetBuilder_3_extract_snippets.py $lean_path

# concatenate the snippets which refers to the same speaker with the same age 
# the script also yields a txt file "./merged_snippets/merged_files.txt"
python3 ./scripts/datasetBuilder_4_concat.py 

# do face recognition tracking and embedding using pyannote
# https://github.com/pyannote/pyannote-video
. ./scripts/datasetBuilder_5_track_embed.sh

# do face clustering
# the images in the "./merged_snippets/cropped_frames" directory are the one we needed for model training
python3 ./scripts/corpus_constructor_6_face_cluster.py 

# cope the output dir to the model data dir
cp -R  merged_snippets/cropped_frames model/data/news



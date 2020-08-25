#!/bin/bash
# https://github.com/pyannote/pyannote-video
echo "Current Directory: $PWD"
# source activate pyannote

for VIDEO_FILE in merged_snippets/*.mp4; do 

	# Virables 
	# VIDEO_FILE="./snippets/s/2018-03-30_0100_US_CNN_Anderson_Cooper_360_merged_Christine_Quinn.mp4"	
	echo $VIDEO_FILE

	length=${#VIDEO_FILE}
	endindex=$(expr $length - 4)

	JSON_FILE="${VIDEO_FILE:0:$endindex}.shots.json"
	echo $JSON_FILE
	TRACK_FILE="${VIDEO_FILE:0:$endindex}.track.txt"
	echo $TRACK_FILE
	LANDMARKS_FILE="${VIDEO_FILE:0:$endindex}.landmarks.txt"
	echo $LANDMARKS_FILE
	EMBEDDING_FILE="${VIDEO_FILE:0:$endindex}.embedding.txt"
	echo $EMBEDDING_FILE


	if test -f $JSON_FILE; then
    	echo $JSON_FILE exists.
	else
		# Shot segmentation
		echo "shot segmenting..."
		pyannote-structure.py shot --verbose $VIDEO_FILE $JSON_FILE
	fi 

	if test -f $TRACK_FILE; then
    	echo $TRACK_FILE exists.
	else
		# Face tracking
		echo "face tracking..."
		pyannote-face.py track --verbose --every=0.5 $VIDEO_FILE $JSON_FILE $TRACK_FILE

	fi 

	if [[ -f $LANDMARKS_FILE ]] && [[ -f $EMBEDDING_FILE ]] ; then
		echo $LANDMARKS_FILE and $EMBEDDING_FILE exists.
	else
		# Facial landmarks and face embedding
		echo "face embedding..."
		MODEL="dlib-models/dlib_face_recognition_resnet_model_v1.dat" # you may need to change it to your own path
		LANDMARKS="dlib-models/shape_predictor_68_face_landmarks.dat"
		pyannote-face.py extract --verbose $VIDEO_FILE $TRACK_FILE $LANDMARKS $MODEL $LANDMARKS_FILE $EMBEDDING_FILE
	fi 

done
# Face clustering
# python3 corpus_constructor_6_cluster_imgcrop.py 








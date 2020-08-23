import os
import math
import time
import cv2 as cv
import numpy as np
from SSRNET.SSRNET_model import SSR_net_general, SSR_net
import argparse
from time import sleep
# This script is adopted and revised from the Agender Project by Pavel Chernov

ROOT_DIR = "./pred"
# Desired width and height to process video.
# Typically it should be smaller than original video frame
# as smaller size significantly speeds up processing almost without affecting quality.
width, height = 550, 300
# Diagonal and line thickness are computed at run-time
diagonal, line_thickness = None, None

# Initialize face detector
face_net = cv.dnn.readNetFromTensorflow(f'{ROOT_DIR}/face_net/opencv_face_detector_uint8.pb', f'{ROOT_DIR}/face_net/opencv_face_detector.pbtxt')

gender_net = None
age_net = None

# Load age and gender models

# Setup global parameters
face_size = 64
face_padding_ratio = 0.10
# Default parameters for SSR-Net
stage_num = [3, 3, 3]
lambda_local = 1
lambda_d = 1
# Initialize gender net
gender_net = SSR_net_general(face_size, stage_num, lambda_local, lambda_d)()
gender_net.load_weights(f'{ROOT_DIR}/SSRNET/ssrnet_gender_3_3_3_64_1.0_1.0.h5')
# Initialize age net
age_net = SSR_net(face_size, stage_num, lambda_local, lambda_d)()
age_net.load_weights(f'{ROOT_DIR}/SSRNET/ssrnet_age_3_3_3_64_1.0_1.0.h5')

def calculateParameters(height_orig, width_orig, cap, output):
    global width, height, diagonal, line_thickness
    area = width * height
    width = int(math.sqrt(area * width_orig / height_orig))
    height = int(math.sqrt(area * height_orig / width_orig))
    # Calculate diagonal
    diagonal = math.sqrt(height * height + width * width)
    # Calculate line thickness to draw boxes
    line_thickness = max(1, int(diagonal / 150))
    # Initialize output video writer
    global out
    fps = cap.get(cv.CAP_PROP_FPS)
    fourcc = cv.VideoWriter_fourcc(*'XVID')
    out = cv.VideoWriter(output, fourcc=fourcc, fps=fps, frameSize=(width, height))
    
def findFaces(img, confidence_threshold=0.7):
    # Get original width and height
    height = img.shape[0]
    width = img.shape[1]
    
    face_boxes = []

    # Convert input image to 3x300x300, as NN model expects only 300x300 RGB images
    blob = cv.dnn.blobFromImage(img, 1.0, (300, 300), mean=(104, 117, 123), swapRB=True, crop=False)

    # Pass blob through model and get detected faces
    face_net.setInput(blob)
    detections = face_net.forward()
    
    for i in range(detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        if (confidence < confidence_threshold):
            continue
        x1 = int(detections[0, 0, i, 3] * width)
        y1 = int(detections[0, 0, i, 4] * height)
        x2 = int(detections[0, 0, i, 5] * width)
        y2 = int(detections[0, 0, i, 6] * height)
        padding_h = int(math.floor(0.5 + (y2 - y1) * face_padding_ratio))
        padding_w = int(math.floor(0.5 + (x2 - x1) * face_padding_ratio))
        x1, y1 = max(0, x1 - padding_w), max(0, y1 - padding_h)
        x2, y2 = min(x2 + padding_w, width - 1), min(y2 + padding_h, height - 1)
        face_boxes.append([x1, y1, x2, y2])

    return face_boxes


def collectFaces(frame, face_boxes, height_orig, width_orig):
    faces = []
    # Process faces
    for i, box in enumerate(face_boxes):
        # Convert box coordinates from resized frame_bgr back to original frame
        box_orig = [
            int(round(box[0] * width_orig / width)),
            int(round(box[1] * height_orig / height)),
            int(round(box[2] * width_orig / width)),
            int(round(box[3] * height_orig / height)),
        ]
        # Extract face box from original frame
        face_bgr = frame[
            max(0, box_orig[1]):min(box_orig[3] + 1, height_orig - 1),
            max(0, box_orig[0]):min(box_orig[2] + 1, width_orig - 1),
            :
        ]
        faces.append(face_bgr)
    return faces


def predictAgeGender(faces):
   
    # Convert faces to N,64,64,3 blob
    blob = np.empty((len(faces), face_size, face_size, 3))
    for i, face_bgr in enumerate(faces):
        blob[i, :, :, :] = cv.resize(face_bgr, (64, 64))
        blob[i, :, :, :] = cv.normalize(blob[i, :, :, :], None, alpha=0, beta=255, norm_type=cv.NORM_MINMAX)
    # Predict gender and age
    genders = gender_net.predict(blob)
    ages = age_net.predict(blob)
    #  Construct labels
    labels = ['{},{}'.format('Male' if (gender >= 0.5) else 'Female', int(age)) for (gender, age) in zip(genders, ages)]
 
    return labels


def get_args():
    parser = argparse.ArgumentParser(description="This script predict the age and gender from the input video"
                                                 "and print the result out on the video",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--video", "-v", type=str, required=True,
                        help="path of the input video")
    parser.add_argument("--output", "-o", type=str, required=True,
                        help="path of the output video")
    args = parser.parse_args()
    return args


def predict(input_path, output):
    # Create a video capture object to read videos
    cap = cv.VideoCapture(input_path)

    # Process video
    paused = False
    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            break

        # Calculate parameters if not yet
        if (diagonal is None):
            height_orig, width_orig = frame.shape[0:2]
            calculateParameters(height_orig, width_orig, cap, output)
            
        # Resize, Convert BGR to HSV
        if ((height, width) != frame.shape[0:2]):
            frame_bgr = cv.resize(frame, dsize=(width, height), fx=0, fy=0)
        else:
            frame_bgr = frame
            
        # Detect faces
        face_boxes = findFaces(frame_bgr)

        # Make a copy of original image
        faces_bgr = frame_bgr.copy()

        if (len(face_boxes) > 0):
            # Draw boxes in faces_bgr image
            for (x1, y1, x2, y2) in face_boxes:
                cv.rectangle(faces_bgr, (x1, y1), (x2, y2), color=(0, 255, 0), thickness=line_thickness, lineType=8)
            
            # Collect all faces into matrix
            faces = collectFaces(frame, face_boxes, height_orig, width_orig)
        
            # Get age and gender
            labels = predictAgeGender(faces)
            
            # Draw labels
            for (label, box) in zip(labels, face_boxes):
                cv.putText(faces_bgr, label, org=(box[0], box[1] - 10), fontFace=cv.FONT_HERSHEY_PLAIN,
                           fontScale=1, color=(0, 64, 255), thickness=1, lineType=cv.LINE_AA)

        # Show frames
        cv.imshow('Source', frame_bgr)
        cv.imshow('Faces', faces_bgr)
        
        # Write output frame
        out.write(faces_bgr)
        
        # Quit on ESC button, pause on SPACE
        key = (cv.waitKey(1 if (not paused) else 0) & 0xFF)
        if (key == 27):
            break
        elif (key == 32):
            paused = (not paused)
        sleep(0.001)
        
    cap.release()
    out.release()
    cv.destroyAllWindows()

if __name__ == '__main__':
    args = get_args()
    input_path = args.video
    output_path = args.output
    if os.path.isfile(input_path) and input_path.endswith('.mp4'):
        predict(input_path, output_path)
        print(f'check the output in {output_path}')
    else: 
        print('invalid path')


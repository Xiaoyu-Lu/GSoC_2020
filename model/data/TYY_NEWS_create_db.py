import numpy as np
import cv2
import argparse
import os


def get_info(file_name):
    tokens = file_name.split('-')
    gender, age = tokens[-2], tokens[-1][:-4]
    return gender, age

def get_args():
    parser = argparse.ArgumentParser(description="This script cleans-up noisy labels "
                                                 "and creates database for training.",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--output", "-o", type=str, required=True,
                        help="path to output database mat file")
    parser.add_argument("--img_size", type=int, default=64,
                        help="output image size")
    args = parser.parse_args()
    return args

def main():
    args = get_args()
    output_path = args.output
    img_size = args.img_size
    # output_path = "news.npz"
    # img_size = 64

    train_set = './news'
    out_genders = []
    out_ages = []
    out_imgs = []
    for root, dirs, files in os.walk(train_set):
        for name in files:
            if name.startswith("."):continue # .DS_Store
            img_path = os.path.join(root, name)
            
            gender, age = get_info(name)
            
            out_genders.append(1 if gender == 'male' else 0)
            out_ages.append(int(age))
            img = cv2.imread(img_path)
            # print(img_path)
            if not img is None:
                out_imgs.append(cv2.resize(img, (img_size, img_size)))

    np.savez(output_path,image=np.array(out_imgs), gender=np.array(out_genders), age=np.array(out_ages), img_size=img_size)


if __name__ == '__main__':
    main()



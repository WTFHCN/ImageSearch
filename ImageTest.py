from sklearn import preprocessing
from scipy.cluster.vq import *
import cv2
import numpy as np
import os
import joblib
from tqdm import tqdm
import FindImage

test_path = "test"  # 训练样本文件夹路径
testing_names = os.listdir(test_path)
image_paths = []
image_set = {}
des_list = []


def test():
    tot_sum = 0
    tot_true = 0
    for name in tqdm(testing_names):
        next_dir = os.path.join(test_path, name)
        if os.path.isdir(next_dir) == True:
            ls = os.listdir(next_dir)
            for testing_name in ls:
                if testing_name.find('.jpg') != -1:
                    image_path = os.path.join(next_dir, testing_name)
                    tot_sum += 1
                    _, image_name = FindImage.search_image(image_path)
                    if image_name == name:
                        tot_true += 1
    print(tot_true, end="")
    print("/", end="")

    print(tot_sum)


def main():
    test()


if __name__ == '__main__':
    main()

from numpy.core.shape_base import vstack
from numpy.lib.function_base import append
from numpy.lib.type_check import imag
from sklearn import preprocessing
from scipy.cluster.vq import *
import cv2
import numpy as np
import os
import joblib
from tqdm import tqdm
import logging

train_path = "train"  # 训练样本文件夹路径


training_names = os.listdir(train_path)
NUM_WORDS = 200  # 聚类中心数
surf_det = cv2.xfeatures2d.SURF_create()

image_paths = []
image_set = {}
des_list = []


def load():
    print("开始读取")
    global image_paths

    for name in tqdm(training_names):
        imageDir = os.path.join(train_path, name)
        if os.path.isdir(imageDir) == True:
            ls = os.listdir(imageDir)
            true_len = 0
            for training_name in ls:
                if training_name.find('.jpg') != -1 or training_name.find('.png') != -1:
                    image_path = os.path.join(imageDir, training_name)
                    image_paths += [image_path]
                    true_len += 1
            image_set[name] = true_len


def get_rgb(img, x, y):
    rgb_f = []
    tot = 255
    rgb_f.append(img[x, y, 0]/tot)
    rgb_f.append(img[x, y, 1]/tot)
    rgb_f.append(img[x, y, 2]/tot)
    return rgb_f


def extraction_KeyPointAndEigenvector(img):
    gray_image = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    kp, des = surf_det.detectAndCompute(gray_image, None)

    points2f = cv2.KeyPoint_convert(kp)
    newdes_list = []
    dx = [-1, 1]
    dy = [1, -1]
    for i in range(len(des)):
        y = int(points2f[i][0])
        x = int(points2f[i][1])

        rgb_tmp = get_rgb(img, x+0, y+0)
        # for px in range(dx):
        #     for py in range(dy):
        #         rgb_tmp = np.hstack((rgb_tmp, get_rgb(img, x+px, y+py)))
        rgb_tmp = np.hstack((rgb_tmp, get_rgb(img, x, y-1)))
        rgb_tmp = np.hstack((rgb_tmp, get_rgb(img, x-1, y)))
        rgb_tmp = np.hstack((rgb_tmp, get_rgb(img, x+1, y)))
        rgb_tmp = np.hstack((rgb_tmp, get_rgb(img, x, y+1)))
        newdes = des[i]
        newdes = np.hstack((newdes, rgb_tmp))
        newdes_list.append(newdes)
    newdes_list = np.array(newdes_list)
    return (kp, newdes_list)


def eigenvector():
    print("提取特征")
    for name, count in tqdm(image_set.items()):
        dir_data = os.path.join(train_path, name)
        if os.path.isdir(dir_data) == True:
            image_list = os.listdir(dir_data)
            for image in image_list:
                filename = os.path.join(dir_data, image)
                if image.find('jpg') != -1 or image.find('png') != -1:
                    logging.debug(filename)
                    img = cv2.imread(filename)
                    if img is None:
                        logging.error(filename)
                        continue
                    kp, des = extraction_KeyPointAndEigenvector(img)
                    des_list.append((filename, des))


def begin_kmeans():
    descriptors = des_list[0][1]

    print('生成向量数组')
    for name, descriptor in tqdm(des_list[1:]):
        # print(name)
        # print(descriptor.shape)
        descriptors = np.vstack((descriptors, descriptor))

    print("开始 k-means 聚类: %d words, %d key points" %
          (NUM_WORDS, descriptors.shape[0]))
    voc, variance = kmeans(descriptors, NUM_WORDS, 1)
    im_features = np.zeros((len(image_paths), NUM_WORDS), "float32")
    for i in tqdm(range(len(image_paths))):
        words, distance = vq(des_list[i][1], voc)
        for w in words:
            im_features[i][w] += 1
    return (im_features, voc, variance)


def save_pkl(im_features, image_paths, voc):
    nbr_occurences = np.sum((im_features > 0) * 1, axis=0)
    idf = np.array(np.log((1.0*len(image_paths)+1) /
                          (1.0*nbr_occurences + 1)), 'float32')
    im_features = im_features*idf
    im_features = preprocessing.normalize(im_features, norm='l2')
    print('保存词袋模型文件')
    joblib.dump((im_features, image_paths, idf, NUM_WORDS, voc),
                "bow.pkl", compress=3)


def main():
    logging.basicConfig(filename="FindFeatures.log",
                        format='%(asctime)s %(filename)s %(levelname)s %(message)s', level=logging.DEBUG, filemode='w')
    load()
    eigenvector()
    im_features, voc, variance = begin_kmeans()
    save_pkl(im_features, image_paths, voc)


if __name__ == '__main__':
    main()

# python findFeatures.py -t dataset/


from os.path import isdir
import cv2
import numpy as np
import os
import joblib
from numpy.core.fromnumeric import sort

from scipy.cluster.vq import *
from sklearn import preprocessing


# parser = ap.ArgumentParser()
# parser.add_argument("-t", "--trainingSet",
#                     help="Path to Training Set", required="True")
# args = vars(parser.parse_args())

# Get the training classes names and store them in a list
train_path = "moeimouto-faces/"  # 训练样本文件夹路径
training_names = os.listdir(train_path)
NUM_WORDS = 200  # 聚类中心数
sift_det = cv2.xfeatures2d.SIFT_create()
image_paths = []
image_set = {}
des_list = []


def extraction_KeyPointAndEigenvector(img):
    gray_image = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)  # 转化为灰度图
    kp, des = sift_det.detectAndCompute(gray_image, None)
    return (kp, des)


def init():
    for name in training_names:
        dir_data = train_path + name
        if os.path.isdir(dir_data) == True:
            image_list = os.listdir(dir_data)
            i = 0
           # image_list.sort()
            for image in image_list:
                if image.find('.png') != -1:
                    lastname = dir_data + "/" + image
                    filename = dir_data + "/image_" + str(i) + ".jpg"
                    print(lastname)
                    os.renames(lastname, filename)
                    i += 1


def eigenvector():
    for name, count in image_set.items():
        dir_data = train_path + name
        if os.path.isdir(dir_data) == True:
            print("从 " + name + " 中提取特征")
            image_list = os.listdir(dir_data)
            for image in image_list:
                filename = dir_data + "/" + image
                if image.find('jpg') != -1:
                    print(filename)
                    kp, des = extraction_KeyPointAndEigenvector(
                        cv2.imread(filename))
                    des_list.append((filename, des))
           # image_list.sort()


def load():
    global image_paths
    for name in training_names[:1]:
        if os.path.isdir(train_path + "/" + name) == True:
            ls = os.listdir(train_path + "/" + name)
            true_len = 0
            for training_name in ls:
                if training_name.find('.jpg') != -1:
                    image_path = os.path.join(train_path + name, training_name)
                    image_paths += [image_path]
                    true_len += 1
            image_set[name] = true_len


def begin_kmeans():
    descriptors = des_list[0][1]
    print('生成向量数组')
    for _, descriptor in des_list[1:]:
        descriptors = np.vstack((descriptors, descriptor))

    print("开始 k-means 聚类: %d words, %d key points" %
          (NUM_WORDS, descriptors.shape[0]))
    voc, variance = kmeans(descriptors, NUM_WORDS, 1)
    im_features = np.zeros((len(image_paths), NUM_WORDS), "float32")
    for i in range(len(image_paths)):
        words, distance = vq(des_list[i][1], voc)

        for w in words:
            im_features[i][w] += 1
    return (im_features, voc, variance)


def save_pkl(im_features, image_paths, voc):
    # Perform Tf-Idf vectorization
    nbr_occurences = np.sum((im_features > 0) * 1, axis=0)
    idf = np.array(np.log((1.0*len(image_paths)+1) /
                          (1.0*nbr_occurences + 1)), 'float32')
    # Perform L2 normalization
    im_features = im_features*idf
    im_features = preprocessing.normalize(im_features, norm='l2')

    print('保存词袋模型文件')
    joblib.dump((im_features, image_paths, idf, NUM_WORDS, voc),
                "bow.pkl", compress=3)


def main():
    # init()
    load()
    eigenvector()
    im_features, voc, variance = begin_kmeans()
    save_pkl(im_features, image_paths, voc)


if __name__ == '__main__':
    main()
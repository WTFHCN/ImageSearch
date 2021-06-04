import cv2
import numpy as np
import joblib
from scipy.cluster.vq import *
import FindFeatures
from sklearn import preprocessing
import numpy as np

from pylab import *

im_features, image_paths, idf, numWords, voc = joblib.load("bow.pkl")


def find_name(str):
    l = 0
    r = 0
    for i in range(len(str)):
        if str[i] == '/':
            l = r
            r = i
    return str[l+1:r]


def search_image(image_path):
    im = cv2.imread(image_path)
    kp, descriptors = FindFeatures.extraction_KeyPointAndEigenvector(im)
    test_features = np.zeros((1, numWords), "float32")
    words, distance = vq(descriptors, voc)
    for w in words:
        test_features[0][w] += 1

    test_features = test_features*idf
    test_features = preprocessing.normalize(test_features, norm='l2')

    score = np.dot(test_features, im_features.T)

    rank_ID = np.argsort(-score)

    ans_list = []
    for i, ID in enumerate(rank_ID[0][0:10]):
        name_path = image_paths[ID]
        name_path = name_path.replace('\\', '/')
        ans_list.append((name_path, find_name(name_path)))
    return ans_list

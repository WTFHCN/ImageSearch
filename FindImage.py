

import cv2
import numpy as np
import joblib
from scipy.cluster.vq import *
import FindFeatures
from sklearn import preprocessing
import numpy as np

from pylab import *


def find_name(str):
    l = 0
    r = 0
    for i in range(len(str)):
        if str[i] == '/':
            l = r
            r = i
    return str[l+1:r]


def search_image(image_path):
    mpl.rcParams['font.sans-serif'] = ['SimHei']
    # Load the classifier, class names, scaler, number of clusters and vocabulary
    im_features, image_paths, idf, numWords, voc = joblib.load("bow.pkl")

    # Create feature extraction and keypoint detector objects
    surf_det = cv2.xfeatures2d.SURF_create()
    # List where all the descriptors are stored
    des_list = []

    im = cv2.imread(image_path)
    kp, des=FindFeatures.extraction_KeyPointAndEigenvector(im)
 
    des_list.append((image_path, des))

    # Stack all the descriptors vertically in a numpy array
    descriptors = des_list[0][1]

    test_features = np.zeros((1, numWords), "float32")
    words, distance = vq(descriptors, voc)
    for w in words:
        test_features[0][w] += 1

    # Perform Tf-Idf vectorization and L2 normalization
    test_features = test_features*idf
    test_features = preprocessing.normalize(test_features, norm='l2')

    score = np.dot(test_features, im_features.T)

    rank_ID = np.argsort(-score)  # 从大到小的索引

    ans_list=[]
    for i, ID in enumerate(rank_ID[0][0:10]):
        str = image_paths[ID]
        str = str.replace('\\', '/')
        ans_list.append((str, find_name(str)))
    return ans_list
    # gray()
    # subplot(5, 5, i+6)
    # imshow(img)
    # title('第%d相似' % (i+1))
    # axis('off')
    # show()

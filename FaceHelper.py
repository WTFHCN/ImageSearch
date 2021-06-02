import cv2
import os
from tqdm import tqdm

data_path = 'data'


def FaceALL():
    image_list = os.listdir(data_path)
    for name in tqdm(image_list):
        face_path = os.path.join(data_path, name+'-face')
        dir_path = os.path.join(os.path.join(data_path, name))
        if os.path.exists(face_path) == False:
            os.mkdir(face_path)
        if os.path.isdir(dir_path) == True:
            image_list = os.listdir(dir_path)
            for name in image_list:
                FindFace(dir_path, name, face_path)


def FindFace(image_path, filename, face_path, cascade_file="lbpcascade_animeface.xml"):
    if not os.path.isfile(cascade_file):
        raise RuntimeError("%s: not found" % cascade_file)
    if filename.find('jpg') != -1 or filename.find('png') != -1:
        cascade = cv2.CascadeClassifier(cascade_file)
        image = cv2.imread(os.path.join(
            image_path, filename), cv2.IMREAD_COLOR)

        if image is None:
            return
        tmp_image = image
        # print(type(image))
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray = cv2.equalizeHist(gray)

        faces = cascade.detectMultiScale(gray,
                                         # detector options
                                         scaleFactor=1.1,
                                         minNeighbors=5,
                                         minSize=(24, 24))
        i = 0

        for (x, y, w, h) in faces:
            # cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)
            tmp_image = image[max(y-h//5, 0):(y+h), max(x-w//5, 0):(x+w)]
            cv2.imwrite(os.path.join(face_path,  str(
                i) + "_" + filename), tmp_image)
            i += 1


if __name__ == '__main__':
    FaceALL()

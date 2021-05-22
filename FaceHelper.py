import cv2
import os
from tqdm import tqdm


image_path = 'datelist'
image_face_path = 'face'


def FaceALL():
    image_list = os.listdir(image_path)
    if os.path.exists(os.path.join(image_path, image_face_path)) == False:
        os.mkdir(os.path.join(image_path, image_face_path))
    for name in tqdm(image_list):
        if os.path.isfile(os.path.join(image_path, name)):
            FindFace(name)


def FindFace(filename, cascade_file="lbpcascade_animeface.xml"):
    if not os.path.isfile(cascade_file):
        raise RuntimeError("%s: not found" % cascade_file)
    if filename.find('jpg') != -1 or filename.find('png') != -1:
        cascade = cv2.CascadeClassifier(cascade_file)
        image = cv2.imread(os.path.join(
            image_path, filename), cv2.IMREAD_COLOR)
        tmp_image = image
        #cv2.imwrite(os.path.join(os.path.join(image_path,image_face_path),filename), tmp_image)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray = cv2.equalizeHist(gray)

        faces = cascade.detectMultiScale(gray,
                                         # detector options
                                         scaleFactor=1.1,
                                         minNeighbors=5,
                                         minSize=(24, 24))
        #image_face = []
        i = 0

        for (x, y, w, h) in faces:
            #cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)
            tmp_image = image[max(y-h//5, 0):(y+h), max(x-w//5, 0):(x+w)]
            cv2.imwrite(os.path.join(os.path.join(
                image_path, image_face_path),  str(i) + "_" + filename), tmp_image)
            i += 1


if __name__ == '__main__':
    FaceALL()

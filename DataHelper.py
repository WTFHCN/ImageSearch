from xpinyin import Pinyin
import os
import shutil
from tqdm import tqdm
date_path = "data"
train_path = "train"
test_path = "test"
trainpercentage = 0.75  # 训练集合与测试百分比


def CheckImage(image_name):
    if image_name.find('.png') != -1 or image_name.find('.jpg') != -1 or image_name.find('.jpeg') != -1:
        return True
    else:
        return False


def RName(str):
    l = 0
    for i in range(len(str)):
        if str[i] <= 'Z' and str[i] >= 'A':
            return str[i:]
        if str[i] <= 'z' and str[i] >= 'a':
            return str[i:]


def DirRename():
    print("中文变拼音")
    imagelist_name = os.listdir(date_path)
    p = Pinyin()
    for name in tqdm(imagelist_name):
        if os.path.isdir(os.path.join(date_path, name)):
            os.rename(os.path.join(date_path, name),
                      os.path.join(date_path, p.get_pinyin(name)))


def Finddata():
    imagelist_name = os.listdir(date_path)
    for name in tqdm(imagelist_name):
        dir_data = os.path.join(date_path, name)
        if os.path.isdir(dir_data) == True:
            image_list = os.listdir(dir_data)
            if len(image_list) < 15:
                print(dir_data)


def PictureRename():
    print("批量重命名")
    imagelist_name = os.listdir(date_path)
    for name in tqdm(imagelist_name):
        dir_data = os.path.join(date_path, name)
        if os.path.isdir(dir_data) == True:
            image_list = os.listdir(dir_data)
            i = 0
            for image in image_list:
                if CheckImage(image):
                    lastname = os.path.join(dir_data, image)
                    # print(lastname)
                    filename = os.path.join(
                        dir_data, "image_" + str(i).zfill(4) + ".jpg")
                    os.renames(lastname, filename)
                    i += 1


def Make_tarin_test():
    print("训练和测试分离")
    imagelist_name = os.listdir(date_path)
    for name in tqdm(imagelist_name):
        dir_data = os.path.join(date_path, name)
        if os.path.isdir(dir_data) == True:

            image_list = os.listdir(dir_data)
            tarinimage_list = os.path.join(train_path, name)
            if os.path.exists(tarinimage_list):
                shutil.rmtree(tarinimage_list)
            os.mkdir(tarinimage_list)

            testimage_list = os.path.join(test_path, name)
            if os.path.exists(testimage_list):
                shutil.rmtree(testimage_list)
            os.mkdir(testimage_list)
            train_num = int(len(image_list)*trainpercentage)

            for image in image_list[:train_num]:
                if image.find('.png') != -1 or image.find('.jpg') != -1:
                    old_name = os.path.join(dir_data, image)
                    new_name = os.path.join(
                        os.path.join(train_path, name), image)
                    shutil.copyfile(old_name, new_name)

            for image in image_list[train_num:]:
                if image.find('.png') != -1 or image.find('.jpg') != -1:
                    old_name = os.path.join(dir_data, image)
                    new_name = os.path.join(
                        os.path.join(test_path, name), image)
                    shutil.copyfile(old_name, new_name)


if __name__ == '__main__':
    # Finddata()
    # PictureRename()
    Make_tarin_test()
    # DirRename()

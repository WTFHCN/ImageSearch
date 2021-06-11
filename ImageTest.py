from scipy.cluster.vq import *
import os
from tqdm import tqdm
import FindImage

test_path = "test"  # 训练样本文件夹路径
result_name = 'result.txt'
image_paths = []
image_set = {}
des_list = []


def test(N):
    print(str(N)+"选1开始测试:")
    testing_names = os.listdir(test_path)
    tot_sum = 0
    tot_true = 0
    result_list = []
    for name in tqdm(testing_names):
        next_dir = os.path.join(test_path, name)
        if os.path.isdir(next_dir) == True:
            ls = os.listdir(next_dir)
            image_sum = 0
            image_true = 0
            for testing_name in ls:
                if testing_name.find('.jpg') != -1 or testing_name.find('.png') != -1:
                    image_path = os.path.join(next_dir, testing_name)
                    tot_sum += 1
                    image_sum += 1
                    image_name = FindImage.search_image(image_path)
                    for i in range(N):
                        if image_name[i][1] == name:
                            tot_true += 1
                            image_true += 1
                            break
            result_list.append((name, image_true, image_sum))

    with open(result_name, 'a') as f:
        for name, A, B in result_list:
            tmp_str = name + "识别率: "+str(format(A/B*100, '.2f') + '%\n')
            f.write(tmp_str)
        tmp_str = "总体" + "识别率: " + \
            str(format(tot_true/tot_sum*100, '.2f') + '%\n')
        f.write(tmp_str)
        f.write('\n\n\n')


def main():
    test(1)
    test(4)
    test(8)


if __name__ == '__main__':
    main()

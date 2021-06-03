import ImageCrawler2
import urllib
image_name_path = "name.txt"
PageNum = 10


def main():
    f = open(image_name_path, 'r', encoding='utf-8')
    name_list = f.read().split('\n')
    f.close()
    # print(len(name_list))
    for name in name_list:
        print("开始爬取"+name)
        print(len(name))
        InputData = urllib.parse.quote(name)
        ImageCrawler2.FindLink(PageNum, InputData, name)


if __name__ == '__main__':
    main()

import ImageCrawler
image_name_path = "name.txt"


def main():
    f = open(image_name_path, 'r', encoding='utf-8')
    name_list = f.read().split('\n')
    f.close()
    # print(len(name_list))
    for name in name_list:
        print("开始爬取"+name)
        print(len(name))
        crawler = ImageCrawler.Crawler(0.05)
        crawler.start(name, 7, 1, 30)


if __name__ == '__main__':
    main()

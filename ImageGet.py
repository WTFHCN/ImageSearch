import ImageCrawler2
import urllib
import ImageCrawler
image_name_path = "name.txt"
PageNum = 5


def main():
    f = open(image_name_path, 'r', encoding='utf-8')
    name_list = f.read().split('\n')
    f.close()
    for name in name_list:
        # print("开始爬取"+name)
        # crawler = ImageCrawler.Crawler(0.05)  # 抓取延迟为 0.05

        # # 抓取关键词为 “美女”，总数为 1 页，开始页码为 2，每页30张（即总共 2*30=60 张）
        # crawler.start(name, 5, 1, 30)
        InputData = urllib.parse.quote(name)
        ImageCrawler2.FindLink(PageNum, InputData, name)


if __name__ == '__main__':
    main()

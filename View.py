
import sys
from PyQt5 import QtWidgets, QtCore, QtGui

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from numpy.core.defchararray import count
import FindImage


class PictureSearch(QWidget):
    def __init__(self):
        super(PictureSearch, self).__init__()
        self.resize(1280, 720)
        self.setWindowTitle("PictureSearch")

        self.palette = QPalette()
        self.back_image = QtGui.QPixmap("image/front_ui.png").scaled(
            self.width(), self.height())
        self.palette.setBrush(QPalette.Background, QBrush(self.back_image))
        self.setPalette(self.palette)
        self.imgName = ""
        self.choose_lable = QLabel(self)
        self.choose_lable.resize(300, 300)
        self.choose_lable.move(80, 100)
        self.choose_lable.setStyleSheet("QLabel{background:white;}")

        self.search_lable = [0]*4
        self.showans_lable = QLabel(self)

        for i in range(4):
            self.search_lable[i] = QLabel(self)
            self.search_lable[i].resize(140, 140)
            self.search_lable[i].setStyleSheet("QLabel{background:white;}")
        self.search_lable[0].move(480, 100)
        self.search_lable[1].move(480+150, 100)
        self.search_lable[2].move(480, 100+150)
        self.search_lable[3].move(480+150, 100+150)

        self.showans_lable.setText("")
        self.showans_lable.resize(180, 30)
        self.showans_lable.move(350, 430)
        self.showans_lable.setStyleSheet("QLabel{background:white;}")

        self.choose_button = QPushButton(self)
        self.choose_button.setText("打开图片")
        self.choose_button.move(130, 30)
        self.choose_button.resize(200, 50)
        self.choose_button.clicked.connect(self.choose_image)

        self.search_button = QPushButton(self)
        self.search_button.setText("检索图片")
        self.search_button.move(520, 30)
        self.search_button.resize(200, 50)
        self.search_button.clicked.connect(self.search_image)

    def choose_image(self):
        self.imgName, imgType = QFileDialog.getOpenFileName(
            self, "打开图片", "", "*.jpg;;*.png;;All Files(*)")
        image = QtGui.QPixmap(self.imgName).scaled(
            self.choose_lable.width(), self.choose_lable.height())
        self.choose_lable.setPixmap(image)

    def find_much_image(datalist):
        name_map = {}
        for find_image, name in datalist:
            if name in name_map:
                name_map[name] += 1
            else:
                name_map[name] = 0

        ans_name = ("", 0)
        for name in name_map:
            # print(name)
            if name_map[name] > ans_name[1]:
                ans_name = (name, int(name_map[name]))

    def search_image(self):
        find_image_list = FindImage.search_image(self.imgName)

        self.showans_lable.setText(find_image_list[0][1])
        for i in range(4):
            find_image, name = find_image_list[i]

            image = QtGui.QPixmap(find_image).scaled(
                self.search_lable[i].width(), self.search_lable[i].height())
            self.search_lable[i].setPixmap(image)
        # print(FindImage.search_image(self.imgName))


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    myshow = PictureSearch()
    myshow.show()
    sys.exit(app.exec_())

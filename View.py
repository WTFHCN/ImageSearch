import sys
from PyQt5 import QtWidgets, QtCore, QtGui

from PyQt5.QtGui import QPalette, QBrush, QPixmap
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import FindImage


class PictureSearch(QWidget):
    def __init__(self):
        super(PictureSearch, self).__init__()
        self.resize(800, 500)
        self.setWindowTitle("PictureSearch")

        self.palette = QPalette()
        self.palette.setBrush(QPalette.Background, QBrush(
            QPixmap("image/background.jpg")))
        self.setPalette(self.palette)
        self.imgName = ""
        self.choose_lable = QLabel(self)
        self.choose_lable.resize(300, 300)
        self.choose_lable.move(80, 100)
        self.choose_lable.setStyleSheet("QLabel{background:white;}")

        self.search_lable = QLabel(self)
        self.search_lable.resize(300, 300)
        self.search_lable.move(480, 100)
        self.search_lable.setStyleSheet("QLabel{background:white;}")

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

    def search_image(self):
        find_image, _ = FindImage.search_image(self.imgName)
        image = QtGui.QPixmap(find_image).scaled(
            self.search_lable.width(), self.search_lable.height())
        self.search_lable.setPixmap(image)
        # print(FindImage.search_image(self.imgName))


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    myshow = PictureSearch()
    myshow.show()
    sys.exit(app.exec_())

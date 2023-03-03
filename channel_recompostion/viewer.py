from PyQt6.QtWidgets import QLabel, QPushButton, QMenu, QWidget, QGridLayout, QVBoxLayout, QFrame, QHBoxLayout
from PyQt6.QtWidgets import QSizePolicy, QSpinBox, QAbstractSpinBox, QApplication
from PyQt6.QtGui import QFont, QIcon, QImage, QPixmap, QDrag
from PyQt6.QtCore import Qt, QSize, QRect, QThread, QPoint, QMimeData
from PyQt6 import QtCore

from image_utils import *
from CR_enum import *

import sys


class ChannelViewer(QLabel):
    def __init__(self, parent=None, ch=Channel.hint, img_data=None):
        super(ChannelViewer, self).__init__(parent)
        self.setScaledContents(True)
        self.setFixedSize(200, 200)
        font = QFont("Microsoft JhengHei", 15, 0, False)
        font.setBold(True)
        self.setFont(font)

        self.main = parent
        self.channel_sign = QLabel(self)
        self.channel_sign.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.ch = ch
        self.data = None

        self.setData(img_data)
        self.setChannel(ch)

    def setData(self, img_data: np.ndarray):
        self.data = img_data
        self.setPixmap(imageToPixmap(img_data))

    def setChannel(self, ch: Channel.hint):
        self.ch = ch
        if ch == Channel.r:
            self.channel_sign.setStyleSheet("color:rgba(255,255,255,200); background-color:rgba(255,0,0,200)")
            self.channel_sign.setText("R")
        elif ch == Channel.g:
            self.channel_sign.setStyleSheet("color:rgba(255,255,255,200); background-color:rgba(0,255,0,200)")
            self.channel_sign.setText("G")
        elif ch == Channel.b:
            self.channel_sign.setStyleSheet("color:rgba(255,255,255,200); background-color:rgba(0,0,255,200)")
            self.channel_sign.setText("B")
        elif ch == Channel.a:
            self.channel_sign.setStyleSheet("color:rgba(255,255,255,200); background-color:rgba(128,128,128,200)")
            self.channel_sign.setText("A")

    def rematch(self):
        self.channel_sign.setGeometry(0, 0, self.width(), int(self.height()/10))

    def resizeEvent(self, a0: QtCore.QSize) -> None:
        self.rematch()


class Window(QWidget):
    def __init__(self):
        super(Window, self).__init__()
        self.ch_viewer = ChannelViewer(self, Channel.r, Image().readImage(r"D:\PhonePicBackUp\head\illust_92911326_20210922_172031.jpg").r())

        self.vbox = QVBoxLayout(self)
        self.vbox.addWidget(self.ch_viewer)


def imageToPixmap(img: np.ndarray) -> QPixmap:
    """
    :param img: only grayscale, rgb, rgba
    :return: QPixmap type
    """
    if len(img.shape) < 3:
        img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGBA)
    elif len(img.shape) == 3:
        img = cv2.cvtColor(img, cv2.COLOR_RGB2RGBA)

    w, h, c = img.shape
    qimg = QImage(img.data.tobytes(), w, h, c*w, QImage.Format.Format_RGBA8888)

    pixmap = QPixmap.fromImage(qimg)
    return pixmap


if __name__ == '__main__':
    app = QApplication([])
    window = Window()
    window.show()
    sys.exit(app.exec())

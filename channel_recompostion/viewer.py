from PyQt6.QtWidgets import QLabel, QPushButton, QMenu, QWidget, QGridLayout, QVBoxLayout, QFrame, QHBoxLayout
from PyQt6.QtWidgets import QSizePolicy, QSpinBox, QAbstractSpinBox, QApplication
from PyQt6.QtGui import QFont, QIcon, QImage, QPixmap, QDrag
from PyQt6.QtCore import Qt, QSize, QRect, QThread, QPoint, QMimeData, QByteArray
from PyQt6 import QtCore

from image_utils import *
from CR_enum import *
from Drag_and_Drop_Overlay import DnDWidget

import sys


class ChannelViewer(QLabel):
    def __init__(self, parent=None, image_viewer=None, ch=Channel.hint, img_data=None, size=200, is_getter=False):
        super(ChannelViewer, self).__init__(parent)
        self.is_getter = is_getter
        self.setScaledContents(True)
        self.setFixedSize(size, size)
        font = QFont("Microsoft JhengHei", 15, 0, False)
        font.setBold(True)
        self.setFont(font)

        self.main = parent
        self.channel_sign = QLabel(self)
        self.channel_sign.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.ch = ch
        self.data = None
        self.name = QLabel(self)
        self.name.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.name.setStyleSheet("color: white; background-color: rgba(0, 0, 0, 0);")

        self.dnd_check = DnDWidget(self)
        self.dnd_check.setStyleSheet("color: rgba(0, 0, 0, 0);background-color: rgba(0, 0, 0, 120);")
        self.dnd_check.raise_()
        self.dnd_check.update.connect(self.getMimeData)
        self.dnd_check.setGeometry(QRect(0, 0, 0, 0))

        self.setLabelName(image_viewer)
        self.setData(img_data)
        self.setChannel(ch)

    def setLabelName(self, image_viewer):
        if image_viewer is not None:
            if type(image_viewer) is str:
                self.name.setText(image_viewer)
            else:
                self.name.setText(image_viewer.name_label.text())
            if self.is_getter is False:
                self.name.setStyleSheet("color: rgba(0,0,0,0); background-color: rgba(0, 0, 0, 0);")
            else:
                self.name.setStyleSheet("color: white; background-color: rgba(0, 0, 0, 128);")

    def setData(self, img_data: np.ndarray):
        if img_data is not None:
            self.data = img_data
            self.setPixmap(imageToPixmap(img_data))

    def setChannel(self, ch: Channel.hint):
        self.channel_sign.setStyleSheet("color:rgba(0,0,0,0); background-color:rgba(0,0,0,0)")
        self.ch = ch
        if ch == Channel.r:
            self.channel_sign.setStyleSheet("color:rgba(255,255,255,200); background-color:rgba(255,0,0,128)")
            self.channel_sign.setText("R")
        elif ch == Channel.g:
            self.channel_sign.setStyleSheet("color:rgba(255,255,255,200); background-color:rgba(0,255,0,128)")
            self.channel_sign.setText("G")
        elif ch == Channel.b:
            self.channel_sign.setStyleSheet("color:rgba(255,255,255,200); background-color:rgba(0,0,255,128)")
            self.channel_sign.setText("B")
        elif ch == Channel.a:
            self.channel_sign.setStyleSheet("color:rgba(255,255,255,200); background-color:rgba(128,128,128,128)")
            self.channel_sign.setText("A")

    def getMimeData(self, data: QMimeData):
        name = data.text()
        ch = Channel(int(data.data("ch")))
        self.setLabelName(name + "-" + str(ch.name).capitalize())
        self.setChannel(Channel(ch))

    def rematch(self):
        self.channel_sign.setGeometry(0, 0, self.width(), int(self.height()/10))
        self.name.setGeometry(0, int(self.height()/10*9), self.width(), int(self.height() / 10))

    def resizeEvent(self, a0: QtCore.QSize) -> None:
        self.rematch()

    def mousePressEvent(self, e) -> None:
        if e.button() == Qt.MouseButton.LeftButton:
            drag = QDrag(self)
            mime_data = QMimeData()
            mime_data.setData("ch", QByteArray(str(self.ch.value).encode("utf-8")))
            mime_data.setText(self.name.text())
            drag.setMimeData(mime_data)

            pixmap = self.pixmap()
            pixmap = pixmap.scaled(100, 100, Qt.AspectRatioMode.KeepAspectRatio)
            qimg = pixmap.toImage()
            qimg.convertToFormat(QImage.Format.Format_RGBA8888)
            ptr = qimg.bits()
            ptr.setsize(qimg.width()*qimg.height()*4)
            array = np.array(ptr).reshape(qimg.height(), qimg.width(), 4)
            array = array[:, :, [2, 1, 0, 3]]
            # breakpoint()
            array = np.uint8(np.float32(array) * 0.7)
            new_qimg = QImage(array.tobytes(), qimg.width(), qimg.height(), QImage.Format.Format_RGBA8888)
            drag.setPixmap(QPixmap.fromImage(new_qimg))
            drop_action = drag.exec()

    def dragEnterEvent(self, e) -> None:
        self.dnd_check.setGeometry(0, 0, self.width(), self.height())


class ImageViewer(QLabel):
    def __init__(self, parent=None, path: str = "", size=420):
        super(ImageViewer, self).__init__(parent)
        self.main = parent
        self.setScaledContents(True)
        self.setFixedSize(size, size)

        self.name_label = QLabel(self)
        font = QFont("Microsoft JhengHei", 15, 0, False)
        font.setBold(True)
        self.name_label.setFont(font)
        self.name_label.setStyleSheet("color: rgba(80, 80, 80, 200);")
        self.name_label.setAlignment(Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignHCenter)
        self.vbox = QVBoxLayout(self)
        self.vbox.addWidget(self.name_label)

        self.image = None

        self.readName(path)
        self.readImage(path, size)

    def readName(self, path):
        self.name_label.setText(os.path.split(path)[1])

    def name(self):
        return self.name_label.text()

    def readImage(self, path, size):
        self.image = Image().readImage(path)
        self.image.resizeKeepRatioX(size)
        self.setPixmap(imageToPixmap(self.image.rgbaData()))

    def data(self):
        return self.image.rgbaData()

    def getChannelData(self, ch: Channel.hint):
        return self.image.getSingleChannel(ch)


class Window(QWidget):
    def __init__(self):
        super(Window, self).__init__()
        # self.image = Image().readImage(r"D:\PhonePicBackUp\head\illust_92911326_20210922_172031.jpg")
        self.ch_viewer_getter = ChannelViewer(self, is_getter=True)
        self.ch_viewer_getter.setStyleSheet("background-color: rgba(0,0,0,50)")
        self.ch_viewer_getter.setAcceptDrops(True)
        self.image_viewer = ImageViewer(self, r"ref\测试.tga")
        self.ch_viewer_r = ChannelViewer(self, self.image_viewer, Channel.r, self.image_viewer.image.r())
        self.ch_viewer_g = ChannelViewer(self, self.image_viewer, Channel.g, self.image_viewer.image.g())
        self.ch_viewer_b = ChannelViewer(self, self.image_viewer, Channel.b, self.image_viewer.image.b())
        self.ch_viewer_a = ChannelViewer(self, self.image_viewer, Channel.a, self.image_viewer.image.a())

        self.ch_frame = QFrame(self)
        self.gbox = QGridLayout(self.ch_frame)
        self.gbox.addWidget(self.ch_viewer_r, 0, 0)
        self.gbox.addWidget(self.ch_viewer_g, 0, 1)
        self.gbox.addWidget(self.ch_viewer_b, 1, 0)
        self.gbox.addWidget(self.ch_viewer_a, 1, 1)

        self.hbox = QHBoxLayout(self)
        self.hbox.addWidget(self.ch_viewer_getter)
        self.hbox.addWidget(self.image_viewer)
        self.hbox.addWidget(self.ch_frame)


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

from PyQt6.QtWidgets import QLabel, QPushButton, QMenu, QWidget, QGridLayout, QVBoxLayout, QFrame, QHBoxLayout, QFileDialog
from PyQt6.QtWidgets import QSizePolicy, QSpinBox, QAbstractSpinBox, QApplication, QLineEdit, QComboBox, QScrollArea
from PyQt6.QtGui import QFont, QIcon, QImage, QPixmap, QDrag, QPalette, QColor
from PyQt6.QtCore import Qt, QSize, QRect, QThread, QPoint, QMimeData, QByteArray
from PyQt6 import QtCore
from ScrollAreaWithStepSettings import ScrollAreaWithStepSettings
from image_utils import *
from CR_enum import *
from Drag_and_Drop_Overlay import DnDWidget

import sys
import Recomp
import GUI_Settings


class ChannelViewer(QLabel):
    def __init__(self, parent=None, image_viewer=None, ch=Channel.hint, size=GUI_Settings.half_picture_size, is_getter=False):
        super(ChannelViewer, self).__init__(parent)
        self.is_getter = is_getter
        self.getter_index = 0
        self.getter_ch = Channel.hint

        if is_getter:
            self.setAcceptDrops(True)
        # self.setScaledContents(True)
        self.setFixedSize(size, size)
        font = QFont("Microsoft JhengHei", GUI_Settings.font_size-2, 0, False)
        font.setBold(True)
        self.setFont(font)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.main = parent
        self.master = image_viewer
        self.ch = ch

        size_po = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        self.channel_sign = QLabel(self)
        self.channel_sign.setSizePolicy(size_po)
        self.channel_sign.setMinimumSize(0, 0)
        self.channel_sign.setAlignment(Qt.AlignmentFlag.AlignCenter)

        font.setPointSize(GUI_Settings.half_font_size)

        self.name_sign = QLabel(self)
        self.name_sign.setSizePolicy(size_po)
        self.name_sign.setFont(font)
        self.name_sign.setWordWrap(True)
        self.name_sign.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.name_sign.setStyleSheet("color: rgba(0, 0, 0, 0); background-color: rgba(0, 0, 0, 0);")

        size_po.setVerticalStretch(1)
        self.frame = QFrame(self)
        self.frame.setSizePolicy(size_po)

        self.vbox = QVBoxLayout(self)
        self.vbox.setStretch(1, 1)
        self.vbox.setContentsMargins(0, 0, 0, 0)
        self.vbox.addWidget(self.channel_sign)
        self.vbox.addWidget(self.frame)
        self.vbox.addWidget(self.name_sign)

        self.dnd_check = DnDWidget(self)
        self.dnd_check.raise_()
        self.dnd_check.update.connect(self.getMimeData)
        self.dnd_check.setGeometry(QRect(0, 0, 0, 0))

        self.setChannel(ch)
        self.setToChild(image_viewer, ch)

    def setLabelName(self, image_viewer):
        if image_viewer is not None:
            if type(image_viewer) is str:
                self.name_sign.setText(image_viewer)
            else:
                self.name_sign.setText(image_viewer.name_label.text())
            if self.is_getter is False:
                self.name_sign.setStyleSheet("color: rgba(0,0,0,0); background-color: rgba(0, 0, 0, 0);")
            else:
                pass
                # self.name_sign.setStyleSheet("color: white; background-color: rgba(0, 0, 0, 128);")

    def setImageFromMaster(self):
        iimg = Recomp.getImageByIndex(self.main.index)
        self.setImage(iimg.image.getSingleChannel(self.ch))
        self.setLabelName(self.master)

    def setImage(self, img_data: np.ndarray):
        if img_data is not None:
            self.setPixmap(imageToPixmap(img_data).scaled(self.width(), self.height(), Qt.AspectRatioMode.KeepAspectRatio))

    def setImageFromImports(self, index, ch: Channel.hint):
        iimg = Recomp.getImageByIndex(index)
        iimg.linkChannel(self)
        self.setImage(iimg.image.getSingleChannel(ch))

    def setChannel(self, ch: Channel.hint):
        if self.channel_sign is self.channel_sign:
            self.channel_sign.setStyleSheet("color:rgba(0,0,0,0); background-color:rgba(0,0,0,0)")
            self.ch = ch
            if ch == Channel.r:
                self.channel_sign.setStyleSheet("color:rgba(255,255,255,200); background-color:rgba(200,0,0,200)")
                self.channel_sign.setText("R")
            elif ch == Channel.g:
                self.channel_sign.setStyleSheet("color:rgba(255,255,255,200); background-color:rgba(0,200,0,200)")
                self.channel_sign.setText("G")
            elif ch == Channel.b:
                self.channel_sign.setStyleSheet("color:rgba(255,255,255,200); background-color:rgba(0,0,200,200)")
                self.channel_sign.setText("B")
            elif ch == Channel.a:
                self.channel_sign.setStyleSheet("color:rgba(255,255,255,200); background-color:rgba(128,128,128,200)")
                self.channel_sign.setText("A")

    def setNameColor(self, ch: Channel.hint):
        if ch == Channel.r:
            self.name_sign.setStyleSheet("color:rgba(255,255,255,200); background-color:rgba(200,0,0,200)")
        elif ch == Channel.g:
            self.name_sign.setStyleSheet("color:rgba(255,255,255,200); background-color:rgba(0,200,0,200)")
        elif ch == Channel.b:
            self.name_sign.setStyleSheet("color:rgba(255,255,255,200); background-color:rgba(0,0,200,200)")
        elif ch == Channel.a:
            self.name_sign.setStyleSheet("color:rgba(255,255,255,200); background-color:rgba(128,128,128,200)")
        elif ch == Channel.hint:
            self.name_sign.setStyleSheet("color:rgba(0,0,0,0); background-color:rgba(0,0,0,0)")

    def setToChild(self, image_v, ch):
        if type(image_v) is ImageViewer:
            self.master = image_v
            image_v.addChild(self, ch)

    def getMimeData(self, data: QMimeData):
        try:
            index = int(data.data("index"))
        except ValueError:
            pass
        else:
            name = data.text()
            iimg = Recomp.getImageByIndex(self.getter_index)
            if iimg is not None:
                iimg.removeLink(self)
            ch = Channel(int(data.data("ch")))
            self.getter_index = index
            self.getter_ch = ch
            self.setLabelName(name + "-" + str(ch.name).capitalize())
            self.setImageFromImports(index, ch)
            self.setNameColor(Channel(ch))
            self.refreshImageView()

    def refreshImageView(self):
        self.master.refreshImage()

    def refresh(self):
        if self.getter_ch != Channel.hint:
            iimg = Recomp.getImageByIndex(self.getter_index)
            self.setPixmap(imageToPixmap(iimg.image.getSingleChannel(self.getter_ch)).scaled(self.width(), self.height(), Qt.AspectRatioMode.KeepAspectRatio))
            self.setLabelName(iimg.name + "-" + str(self.getter_ch.name).capitalize())
            self.master.addRefreshFlag()

    def clearSelf(self, remove=True):
        if self.is_getter:
            iimg = Recomp.getImageByIndex(self.getter_index)
            if iimg is not None:
                if remove:
                    iimg.removeLink(self)
                self.setPixmap(QPixmap())
                self.getter_ch = Channel.hint
                self.getter_index = 0
                self.setNameColor(Channel.hint)
                self.refreshImageView()

    def rematch(self):
        pass

    def resizeEvent(self, a0: QtCore.QSize) -> None:
        self.rematch()

    def mousePressEvent(self, e) -> None:
        if e.button() == Qt.MouseButton.LeftButton and not self.is_getter and not self.pixmap().isNull():
            drag = QDrag(self)
            mime_data = QMimeData()
            mime_data.setData("ch", QByteArray(str(self.ch.value).encode("utf-8")))
            mime_data.setData("index", QByteArray(str(self.main.index).encode("utf-8")))
            mime_data.setText(self.name_sign.text())
            drag.setMimeData(mime_data)

            drag.setPixmap(pixmapWithAlpha(self.pixmap()))
            drop_action = drag.exec()

    def contextMenuEvent(self, e) -> None:
        if self.is_getter:
            cmenu = QMenu(self)
            remove_pixmap = cmenu.addAction("Clear")

            pos = self.mapToGlobal(e.pos())
            pos.setY(pos.y() - 5)
            pos.setX(pos.x() - 2)
            action = cmenu.exec(pos)
            if action == remove_pixmap:
                self.clearSelf()

    def dragEnterEvent(self, e) -> None:
        self.dnd_check.setGeometry(0, 0, self.width(), self.height())

    def dragLeaveEvent(self, e) -> None:
        self.dnd_check.setGeometry(0, 0, 0, 0)


class ImageViewer(QLabel):
    def __init__(self, parent, size=GUI_Settings.picture_size, is_getter=False):
        super(ImageViewer, self).__init__(parent)
        self.main = parent
        self.is_getter = is_getter
        self.setFixedSize(size, size)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.ch_viewers = [ChannelViewer()] * 4
        # self.ch_viewers.clear()
        self.refresh_flag = 0

        self.name_label = QLineEdit(self)

        if not is_getter:
            self.name_label.deleteLater()
            self.name_label = QLabel(self)
            self.name_label.setWordWrap(True)
            self.name_label.setTextInteractionFlags(Qt.TextInteractionFlag.TextBrowserInteraction)
            self.name_label.setStyleSheet("color: rgba(210, 210, 210, 200);background-color: rgba(0, 0, 0, 150);border-radius: 0px")
        else:
            self.name_label.setStyleSheet("color: rgba(40, 40, 40, 200);background-color: rgba(255, 255, 255, 150);border-radius: 0px")

        font = QFont("Microsoft JhengHei", GUI_Settings.font_size, 0, False)
        font.setBold(True)
        self.name_label.setFont(font)
        self.name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        size_po = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.MinimumExpanding)
        self.name_label.setSizePolicy(size_po)

        size_po.setVerticalStretch(1)
        self.frame = QFrame(self)
        self.frame.setSizePolicy(size_po)

        self.vbox = QVBoxLayout(self)
        self.vbox.setAlignment(Qt.AlignmentFlag.AlignBottom)
        self.vbox.setContentsMargins(0, 0, 0, 0)
        self.vbox.addWidget(self.frame)
        self.vbox.addWidget(self.name_label)

    def setFileName(self, path):
        if path != "":
            name = os.path.split(path)[1]
            wrapers = ["_", "-", ".", ]
            for wrap in wrapers:
                name = name.replace(wrap, f"{wrap}\u200b")
            self.name_label.setText(name)

    def name(self):
        return self.name_label.text()

    def setImage(self, img: Image):
        self.setPixmap(imageToPixmap(img.rgbaData()).scaled(self.width(), self.height(), Qt.AspectRatioMode.KeepAspectRatio))

    def refreshImage(self):
        if self.is_getter:
            x = y = 1
            for i in range(4):
                index = self.ch_viewers[i].getter_index
                ch = self.ch_viewers[i].getter_ch
                if ch == Channel.hint:
                    continue
                c_img = Recomp.getImageByIndex(index).image.getSingleChannel(ch)

                x = max(x, c_img.shape[1])
                y = max(y, c_img.shape[0])

            img = rgbaImage(x, y, dtype=np.uint8)
            img[:, :, 3] = singleChannelImage(x, y, black_or_white=1)
            for i in range(4):
                index = self.ch_viewers[i].getter_index
                ch = self.ch_viewers[i].getter_ch
                if ch == Channel.hint:
                    continue
                img[:, :, i] = convertToU8(Recomp.getImageByIndex(index).image.resized((x, y)).getSingleChannel(ch))
            self.setPixmap(imageToPixmap(img).scaled(self.width(), self.height(), Qt.AspectRatioMode.KeepAspectRatio))
        else:
            pass

    def addRefreshFlag(self):
        self.refresh_flag += 1

    def checkedRefresh(self):
        if self.refresh_flag != 0:
            self.refreshImage()
            self.refresh_flag = 0

    def addChild(self, ch_v: ChannelViewer, ch: Channel.hint):
        if ch == Channel.r:
            self.ch_viewers[0] = ch_v
        elif ch == Channel.g:
            self.ch_viewers[1] = ch_v
        elif ch == Channel.b:
            self.ch_viewers[2] = ch_v
        elif ch == Channel.a:
            self.ch_viewers[3] = ch_v

    def data(self):
        if not self.is_getter:
            return Recomp.getImageByIndex(self.main.index).image.rgbaData()

    def getChannelData(self, ch: Channel.hint):
        return Recomp.getImageByIndex(self.main.index).image.getSingleChannel(ch)

    def deleteSelf(self):

        self.deleteLater()


def imageToPixmap(img: np.ndarray) -> QPixmap:
    """
    :param img: only grayscale, rgb, rgba
    :return: QPixmap type
    """
    # print(img.shape)
    if len(img.shape) < 3:
        img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGBA)
    elif len(img.shape) == 3:
        img = cv2.cvtColor(img, cv2.COLOR_RGB2RGBA)
    img = convertToU8(img)
    h, w, c = img.shape
    qimg = QImage(img.data.tobytes(), w, h, c*w, QImage.Format.Format_RGBA8888)

    pixmap = QPixmap.fromImage(qimg)
    return pixmap


def pixmapWithAlpha(pixmap: QPixmap):
    pixmap = pixmap.scaled(100, 100, Qt.AspectRatioMode.KeepAspectRatio)
    qimg = pixmap.toImage()
    qimg.convertToFormat(QImage.Format.Format_RGBA8888)
    ptr = qimg.bits()
    ptr.setsize(qimg.width() * qimg.height() * 4)
    array = np.array(ptr).reshape(qimg.height(), qimg.width(), 4)
    array = array[:, :, [2, 1, 0, 3]]
    # breakpoint()
    array = np.uint8(np.float32(array) * 0.7)
    new_qimg = QImage(array.tobytes(), qimg.width(), qimg.height(), QImage.Format.Format_RGBA8888)
    new_pix = QPixmap.fromImage(new_qimg)
    return new_pix




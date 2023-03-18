from PyQt6.QtWidgets import QFileDialog
from PyQt6.QtGui import QImage, QPixmap
from PyQt6.QtCore import Qt
from image_utils import *


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


def openReadOnlyFileDialog():
    dialog = QFileDialog()
    dialog.setFileMode(QFileDialog.FileMode.ExistingFile)
    dialog.setNameFilters(["All(*)", "Picture (*.jpg)", "Picture (*.png)", "Picture (*.tga)", "Picture (*.webp)"])
    dialog.setDirectory(os.path.abspath("../"))
    if dialog.exec():
        file_path = dialog.selectedFiles()[0]
        return file_path
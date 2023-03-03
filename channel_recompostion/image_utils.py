"""


"""
import cv2
import numpy as np
import os


class Image:
    def __init__(self, img_data: np.ndarray=None):
        self.img = img_data
        if self.img is not None:
            self.channel_count = self.__getChannelCount()

    def setImageData(self, img_data: np.ndarray):
        self.img = img_data
        self.channel_count = self.__getChannelCount()

    def readImage(self, path):
        self.img = cv_imread(path)
        self.channel_count = self.__getChannelCount()
        return self

    def writeImage(self, path):
        cv_imwrite(path, self.img)

    def data(self):
        """
        it's bgr(a) data
        :return:
        """
        return self.img

    def shape(self):
        """
        shape will be (y, x, channel_count) or (y, x) if channel_count = 1
        """
        return self.img.shape

    def resolution(self):
        return self.shape()[0:2]

    def dtype(self):
        return self.img.dtype

    def zeroData(self):
        """
        :return: same res single channel image(np.ndarray)
        """
        return np.zeros(self.resolution(), self.dtype())

    def whiteData(self):
        return np.full(self.resolution(), 255, dtype=self.dtype())

    def r(self):
        if self.channel_count >= 3:
            return self.img[:, :, 2]
        else:
            return self.img

    def g(self):
        if self.channel_count >= 3:
            return self.img[:, :, 1]
        else:
            return self.zeroData()

    def b(self):
        if self.channel_count >= 3:
            return self.img[:, :, 0]
        else:
            return self.zeroData()

    def a(self):
        if self.channel_count >= 4:
            return self.img[:, :, 3]
        else:
            return self.zeroData()

    def __getChannelCount(self):
        try:
            count = self.shape()[2]
        except Exception as e:
            print(e)
            count = 1

        return count

    def resize(self, dsize, fx=None, fy=None, interpolation=None):
        """
        :param dsize: should be (y, x), or be None/(0, 0) and use fx fy to implement
        :param fx: x ratio
        :param fy: y ratio
        :param interpolation: opencv interpolation enumeration
        """
        self.img = cv2.resize(self.img, dsize, fx=fx, fy=fy, interpolation=interpolation)

    def resizeKeepRatioX(self, x, interpolation=None):
        ratio = self.resolution()[0]/self.resolution()[1]
        y = int(x * ratio)
        self.img = cv2.resize(self.img, (x, y), interpolation=interpolation)

    def resizeKeepRatioY(self, y,  interpolation=None):
        ratio = self.resolution()[1] / self.resolution()[0]
        x = int(y * ratio)
        self.img = cv2.resize(self.img, (x, y), interpolation=interpolation)

    def rgbData(self):
        if self.channel_count > 1:
            return cv2.cvtColor(self.img, cv2.COLOR_BGR2RGB)
        else:
            return cv2.cvtColor(self.img, cv2.COLOR_GRAY2RGB)

    def rgbaData(self):
        if self.channel_count > 3:
            return cv2.cvtColor(self.img, cv2.COLOR_BGRA2RGBA)
        elif self.channel_count > 1:
            return cv2.cvtColor(self.img, cv2.COLOR_BGR2RGBA)
        else:
            return cv2.cvtColor(self.img, cv2.COLOR_GRAY2RGBA)

    def bgrData(self):
        if self.channel_count > 1:
            return self.img
        else:
            return cv2.cvtColor(self.img, cv2.COLOR_GRAY2BGR)

    def bgraData(self):
        if self.channel_count > 3:
            return self.img
        elif self.channel_count > 1:
            return cv2.cvtColor(self.img, cv2.COLOR_BGR2BGRA)
        else:
            return cv2.cvtColor(self.img, cv2.COLOR_GRAY2BGRA)


def cv_imread(file_path):
    """
    :param file_path: image path
    :return: opencv image, also numpy array, will be a BGR(A) ordered array
    """
    cv_img = cv2.imdecode(np.fromfile(file_path, dtype=np.uint8), -1)
    return cv_img


def cv_imwrite(file_path: str, img: np.ndarray):
    [filename, extension] = os.path.splitext(file_path)
    cv2.imencode(extension, img)[1].tofile(file_path)


def cv_imshow(img: np.ndarray, win_name="ww", wait_key=0):
    cv2.imshow(win_name, img)
    cv2.waitKey(wait_key)


def notNone(obj) -> bool:
    return obj is not None


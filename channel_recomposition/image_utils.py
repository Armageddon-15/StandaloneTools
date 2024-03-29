"""


"""
import imageio.v3 as iio
import cv2
import numpy as np
import os

from CR_Enum import *
from CR_Error import *


class Image:
    def __init__(self, img_data: np.ndarray = None):
        self.img = None
        if img_data is not None:
            self.img = convertToF32(img_data)
        self.channel_count = 0
        if self.img is not None:
            self.channel_count = self.__getChannelCount()

    def setImageData(self, img_data: np.ndarray):
        self.img = img_data.copy()
        self.channel_count = self.__getChannelCount()

    def readImage(self, path):
        try:
            self.img = convertToF32(imread(path))
        except ValueError:
            raise FileShouldBeEnglishOnly("filename and path should be english only\n"
                                          "路径和文件名必须为英文")
        # print(self.img, self.img.dtype)
        self.channel_count = self.__getChannelCount()
        return self

    def writeImage(self, path, ch=Channel.all, black_or_white=1):
        """
        save image,
        :param path: path
        :param ch: channel enumeration
        :param black_or_white: 0 is black, 1 is white
        """
        imwrite(path, self.rgbaWithSelection(ch, black_or_white))

    def rgbaWithSelection(self, ch=Channel.all, black_or_white=1):
        """
        always return rgba 4 channels
        :param ch: channel enumeration
        :param black_or_white: 0 is black, 1 is white
        :return: image np.ndarray
        """
        img = self.img.copy()
        for n in range(3):
            bit = ch >> n
            # print(bin(bit))
            if bit & 0b0001 != 0b0001:
                # print("bb")
                img[:, :, n] = self.zeroData()

        if ch & 0b1000 != 0b1000:
            img[:, :, 3] = self.whiteData() if black_or_white else self.zeroData()

        return img

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
            return self.img[:, :, 0]
        else:
            return self.img

    def g(self):
        if self.channel_count >= 3:
            return self.img[:, :, 1]
        else:
            return self.zeroData()

    def b(self):
        if self.channel_count >= 3:
            return self.img[:, :, 2]
        else:
            return self.zeroData()

    def a(self):
        if self.channel_count >= 4:
            return self.img[:, :, 3]
        else:
            return self.zeroData()

    def getSingleChannel(self, ch: Channel.hint):
        if ch == Channel.r:
            return self.r()
        elif ch == Channel.g:
            return self.g()
        elif ch == Channel.b:
            return self.b()
        elif ch == Channel.a:
            return self.a()

    def __getChannelCount(self):
        try:
            # print(self.shape())
            count = self.shape()[2]
        except IndexError:
            # print("It's grayscale image")
            count = 1

        return count

    def resize(self, dsize, fx=None, fy=None, interpolation=cv2.INTER_LINEAR):
        """
        :param dsize: should be (y, x), or be None/(0, 0) and use fx fy to implement
        :param fx: x ratio
        :param fy: y ratio
        :param interpolation: opencv interpolation enumeration, default is cv2.INTER_LINEAR
        """
        self.img = cv2.resize(self.img, dsize, fx=fx, fy=fy, interpolation=interpolation)

    def resizeKeepRatioX(self, x, interpolation=cv2.INTER_LINEAR):
        ratio = self.resolution()[0]/self.resolution()[1]
        y = int(x * ratio)
        self.img = cv2.resize(self.img, (x, y), interpolation=interpolation)

    def resizeKeepRatioY(self, y,  interpolation=cv2.INTER_LINEAR):
        ratio = self.resolution()[1] / self.resolution()[0]
        x = int(y * ratio)
        self.img = cv2.resize(self.img, (x, y), interpolation=interpolation)

    def resized(self, dsize, fx=None, fy=None, interpolation=cv2.INTER_LINEAR):
        """
        :param dsize: should be (y, x), or be None/(0, 0) and use fx fy to implement
        :param fx: x ratio
        :param fy: y ratio
        :param interpolation: opencv interpolation enumeration, default is cv2.INTER_LINEAR
        """
        return Image(cv2.resize(self.img, dsize, fx=fx, fy=fy, interpolation=interpolation))

    def resizedKeepRatioX(self, x, interpolation=cv2.INTER_LINEAR):
        ratio = self.resolution()[0]/self.resolution()[1]
        y = int(x * ratio)
        return Image(cv2.resize(self.img, (x, y), interpolation=interpolation))

    def resizedKeepRatioY(self, y,  interpolation=cv2.INTER_LINEAR):
        ratio = self.resolution()[1] / self.resolution()[0]
        x = int(y * ratio)
        return Image(cv2.resize(self.img, (x, y), interpolation=interpolation))

    def rgbData(self):
        if self.channel_count == 1:
            return cv2.cvtColor(self.img, cv2.COLOR_GRAY2RGB)
        elif self.channel_count == 3:
            return self.img
        else:
            return cv2.cvtColor(self.img, cv2.COLOR_RGBA2RGB)

    def rgbaData(self):
        # print(self.channel_count)
        if self.channel_count == 4:
            return self.img
        elif self.channel_count == 3:
            return cv2.cvtColor(self.img, cv2.COLOR_RGB2RGBA)
        else:
            return cv2.cvtColor(self.img, cv2.COLOR_GRAY2RGBA)

    def bgrData(self):
        if self.channel_count == 1:
            return cv2.cvtColor(self.img, cv2.COLOR_GRAY2BGR)
        elif self.channel_count == 3:
            return cv2.cvtColor(self.img, cv2.COLOR_RGB2BGR)
        else:
            return cv2.cvtColor(self.img, cv2.COLOR_RGBA2BGR)

    def bgraData(self):
        if self.channel_count == 1:
            return cv2.cvtColor(self.img, cv2.COLOR_GRAY2BGRA)
        elif self.channel_count == 3:
            return cv2.cvtColor(self.img, cv2.COLOR_RGB2BGRA)
        else:
            return cv2.cvtColor(self.img, cv2.COLOR_RGBA2BGRA)


def cv_imread(file_path):
    """
    :param file_path: image path
    :return: opencv image, also numpy array, will be a BGR(A) ordered array
    """
    cv_img = cv2.imdecode(np.fromfile(file_path), -1)
    return cv_img


def imread(file_path: str):
    """
    :param file_path: image path
    :return: numpy array, will be an RGB(A) ordered array
    """
    img = iio.imread(file_path)
    return img


def cv_imwrite(file_path: str, img: np.ndarray):
    [filename, extension] = os.path.splitext(file_path)
    cv2.imencode(extension, img)[1].tofile(file_path)


def imwrite(file_path: str, img: np.ndarray):
    iio.imwrite(file_path, img)


def cv_imshow(img: np.ndarray, win_name="ww", wait_key=0):
    cv2.imshow(win_name, img)
    cv2.waitKey(wait_key)


def rgbaImage(x, y, black_or_white=0, *args, **kwargs):
    if black_or_white == 0:
        return np.zeros((y, x, 4), *args, **kwargs)
    elif black_or_white == 1:
        return np.full((y, x, 4), 255, *args, **kwargs)


def rgbImage(x, y, black_or_white=0, *args, **kwargs):
    if black_or_white == 0:
        return np.zeros((y, x, 3), *args, **kwargs)
    elif black_or_white == 1:
        return np.full((y, x, 3), 255, *args, **kwargs)


def singleChannelImage(x, y, black_or_white=0, data_type: Bit.hint = Bit.hint, *args, **kwargs):
    if black_or_white == 0:
        return np.zeros((y, x), *args, **kwargs)
    elif black_or_white == 1:
        return np.full((y, x), getTypeMaximum(data_type), *args, **kwargs)


def getTypeMaximum(dtype):
    if dtype == Bit.hint or dtype == Bit.U8:
        return 255
    elif dtype == Bit.U16:
        return 65535
    elif dtype == Bit.F32:
        return 1.0


def convertToF32(img: np.ndarray) -> np.ndarray:
    # print(img, img.dtype)
    if img.dtype == "uint8" or img.dtype == "int8":
        return np.float32(img/255)
    elif img.dtype == "uint16" or img.dtype == "int16" or img.dtype == "uint32" or img.dtype == "int32":
        return np.float32(img/65535)
    else:
        return np.float32(img)


def convertToU16(img: np.ndarray) -> np.ndarray:
    if img.dtype == "uint8" or img.dtype == "int8":
        return np.uint16(img*255)
    elif img.dtype == "float32" or img.dtype == "float64":
        return np.uint16(img*65535)
    else:
        return np.uint16(img)


def convertToU8(img: np.ndarray) -> np.ndarray:
    if img.dtype == "uint16" or img.dtype == "int16" or img.dtype == "uint32" or img.dtype == "int32":
        return np.uint8(img / 255)
    elif img.dtype == "float32" or img.dtype == "float64":
        return np.uint8(img * 255)
    else:
        return np.uint8(img)


def notNone(obj) -> bool:
    return obj is not None


"""
settings for gui
"""
import json
from CR_enum import *


class SettingValue:
    def __init__(self, va):
        self.__value = va

    def setValue(self, va):
        self.__value = va

    def getValue(self):
        return self.__value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, va):
        self.__value = va

    def __add__(self, other):
        return other + self.__value

    def __radd__(self, other):
        return self.__value + other

    def __iadd__(self, other):
        return self.__value + other

    def __sub__(self, other):
        return self.__value - other

    def __rsub__(self, other):
        return other - self.__value

    def __isub__(self, other):
        return self.__value - other

    def __mul__(self, other):
        return other * self.__value

    def __rmul__(self, other):
        return other * self.__value

    def __imul__(self, other):
        return other * self.__value

    def __truediv__(self, other):
        return self.__value / other

    def __rtruediv__(self, other):
        return other / self.__value

    def __idiv__(self, other):
        return self.__value / other

    def __floordiv__(self, other):
        return self.__value // other

    def __rfloordiv__(self, other):
        return other // self.__value

    def __ifloordiv__(self, other):
        return self.__value // other

    def __mod__(self, other):
        return self.__value % other

    def __rmod__(self, other):
        return other % self.__value

    def __imod__(self, other):
        return self.__value % other

    def __lt__(self, other):
        return self.__value < other

    def __le__(self, other):
        return self.__value <= other

    def __eq__(self, other):
        return self.__value == other

    def __ne__(self, other):
        return self.__value != other

    def __gt__(self, other):
        return self.__value > other

    def __ge__(self, other):
        return self.__value >= other

    def __int__(self):
        return int(self.__value)

    # def __str__(self):
    #     return str(self.__value)


class BaseSetting:
    def toJson(self):
        d = {}
        for key in self.__dict__.keys():
            d.update({key: self.__dict__[key].getValue()})
        return d

    def toAttribute(self, json_dict):
        for key in self.__dict__.keys():
            self.__dict__[key].setValue(json_dict[key].getValue())


# detail
class Detail(BaseSetting):
    def __init__(self):
        self.picture_size = SettingValue(300)
        self.half_picture_size = SettingValue(145)
        self.font_size = SettingValue(15)
        self.half_font_size = SettingValue(8)


class ImageFormat(BaseSetting):
    def __init__(self):
        self.res_x = SettingValue(0)
        self.res_y = SettingValue(0)
        self.format = SettingValue("png")
        self.interpolation = SettingValue("nearest")
        self.bit = SettingValue("8")


# window
class Window(BaseSetting):
    def __init__(self):
        self.use_this = SettingValue(False)
        self.x = SettingValue(0)
        self.y = SettingValue(0)
        self.width = SettingValue(1000)
        self.height = SettingValue(800)

    def setGeo(self, x, y, width, height):
        self.x = SettingValue(x)
        self.y = SettingValue(y)
        self.width = SettingValue(width)
        self.height = SettingValue(height)


def saveSettings():
    global a_dict
    a_dict = {"window": win_setting.toJson(),
              "detail": detail_setting.toJson(),
              "image": image_setting.toJson()}

    with open("GUI_Setting.json", "w") as json_file:
        json.dump(a_dict, json_file, indent=4)


def readSettings():
    global detail_setting, win_setting, image_setting, a_dict
    with open("GUI_Setting.json", "r") as json_file:
        a_dict = json.load(json_file)
        for setting_class in a_dict.keys():
            for setting in a_dict[setting_class].keys():
                a_dict[setting_class][setting] = SettingValue(a_dict[setting_class][setting])

    win_setting.toAttribute(a_dict["window"])
    detail_setting.toAttribute(a_dict["detail"])
    image_setting.toAttribute(a_dict["image"])


def saveAndLoad():
    saveSettings()
    readSettings()


detail_setting = Detail()
win_setting = Window()
image_setting = ImageFormat()

a_dict = dict()

try:
    readSettings()
except json.decoder.JSONDecodeError:
    saveAndLoad()
except KeyError:
    saveAndLoad()
except FileNotFoundError:
    saveAndLoad()


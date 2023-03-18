from image_utils import *
import math


import_images = {}
export_images = []


class IndexedImage:
    def __init__(self, image: Image, name="", index=0):
        self.image = image
        self.index = index
        self.name = name

        self.linkers = set()

    def linkChannel(self, ch_v):
        self.linkers.add(ch_v)

    def removeLink(self, ch_v):
        self.linkers.discard(ch_v)

    def clearLinkers(self):
        self.linkers.clear()

    def update(self, image: Image, name=""):
        self.image = image
        self.name = name


class Recompositer:
    def __init__(self):
        self.ch_imgs = [None] * 4
        self.res_x = 0
        self.res_y = 0
        self.count = 0

    def setChannelImage(self, img: np.ndarray, ch: Channel.hint):
        if ch != Channel.hint:
            index = int(math.log2(int(ch.value)))
            self.ch_imgs[index] = img

    def resize(self, x, y, interpolation=cv2.INTER_LINEAR):
        if min(x, y) == 0:
            x = y = 0
            for img in self.ch_imgs:
                if img is not None:
                    self.count += 1
                    x = max(img.shape[1], x)
                    y = max(img.shape[0], y)

        self.res_x = x
        self.res_y = y
        for n in range(4):
            if self.ch_imgs[n] is not None:
                self.ch_imgs[n] = cv2.resize(self.ch_imgs[n], (x, y), interpolation=interpolation)

    def composite(self, path, name, form, bit: Bit.hint):
        if min(self.res_x, self.res_y) <= 0:
            return None
        if self.count == 1:
            c_img = singleChannelImage(self.res_x, self.res_y, 1, dtype=Bit.F32)
            for n in range(4):
                if self.ch_imgs[n] is not None:
                    c_img = self.ch_imgs[n]

        else:
            c_img = rgbaImage(self.res_x, self.res_y, dtype=np.float32)
            c_img[:, :, 3] = singleChannelImage(self.res_x, self.res_y, 1, dtype=Bit.F32)

            for n in range(4):
                if self.ch_imgs[n] is not None:
                    c_img[:, :, n] = self.ch_imgs[n]

        convert_function = chooseConvertFunction(bit, form, self.count)

        c_img = convert_function(c_img)

        if name == "":
            name = "no_title"
        makeDir(path)
        imwrite(os.path.join(path, name+"."+form), c_img)


def makeDir(path):
    if not os.path.exists(path):
        try:
            os.makedirs(path)
        except Exception as e:
            print(e)


def chooseConvertFunction(bit: Bit.hint, form: str, ch_count: int):
    func = None
    format_dic = {Bit.U8: {"jpg", "png", "webp", "tiff", "tga"}, Bit.U16: {"tiff"},
                  Bit.U16_1: {"png", "tiff"},  Bit.F32: {"tiff"}}
    if ch_count == 1 and bit == Bit.U16:
        bit = Bit.U16_1

    if form in format_dic[bit]:
        if bit == Bit.U8:
            func = convertToU8
        elif bit == Bit.U16 or bit == Bit.U16_1:
            func = convertToU16
        elif bit == Bit.F32:
            func = convertToF32
    else:
        if ch_count == 1 and bit == Bit.F32:
            func = chooseConvertFunction(Bit.U16_1, form, ch_count)
        else:
            func = chooseConvertFunction(Bit.U8, form, ch_count)

    return func


def convertJsonStringToBit(st: str):
    if st == "8":
        return Bit.U8
    elif st == "16":
        return Bit.U16
    elif st == "32":
        return Bit.F32
    else:
        raise ValueError(f"no this bit method: {st}")


def convertJsonStringToInterp(st: str):
    convert_dic = {"linear": cv2.INTER_LINEAR, "cubic": cv2.INTER_CUBIC, "lanczos4": cv2.INTER_LANCZOS4, "nearest": cv2.INTER_NEAREST}
    if st in convert_dic:
        return convert_dic[st]
    else:
        raise ValueError(f"no this interpolation: {st}")


def getImageByIndex(index, images=None) -> IndexedImage:
    if images is None:
        images = import_images
    for key, va in images.items():
        if va.index == index:
            return va


def removeImageByIndex(index):
    import_images.pop(index)


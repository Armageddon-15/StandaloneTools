from image_utils import *


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


def getImageByIndex(index, images=None) -> IndexedImage:
    if images is None:
        images = import_images
    for key, va in images.items():
        if va.index == index:
            return va





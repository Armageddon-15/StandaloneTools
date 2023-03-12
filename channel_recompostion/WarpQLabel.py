from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPainter
from PyQt6.QtWidgets import QLabel, QStyleOption, QStyle


class SuperQLabel(QLabel):
    def __init__(self, *args, **kwargs):
        super(SuperQLabel, self).__init__(*args, **kwargs)
        self.__text_alignment = None

    def setTextAlignment(self, alignment: int):
        self.__text_alignment = alignment

    def paintEvent(self, event):
        super(SuperQLabel, self).paintEvent(event)
        opt = QStyleOption()
        opt.initFrom(self)
        painter = QPainter(self)

        self.style().drawPrimitive(QStyle.PrimitiveElement.PE_Widget, opt, painter, self)

        self.style().drawItemText(painter, self.rect(),
                                  self.__text_alignment, self.palette(), True, self.text())
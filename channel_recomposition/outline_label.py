import sys
import math
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *


class OutlinedLabel(QLabel):

    def __init__(self, parent, *args):
        super().__init__(parent, *args)
        self.w = 1 / 25
        self.mode = True
        self.setBrush(Qt.GlobalColor.white)
        self.setPen(Qt.GlobalColor.black)

    def scaledOutlineMode(self):
        return self.mode

    def setScaledOutlineMode(self, state):
        self.mode = state

    def outlineThickness(self):
        return self.w * self.font().pointSize() if self.mode else self.w

    def setOutlineThickness(self, value):
        self.w = value

    def setBrush(self, brush):
        if not isinstance(brush, QBrush):
            brush = QBrush(brush)
        self.brush = brush

    def setPen(self, pen):
        # if not isinstance(pen, QPen):
        pen = QPen(pen)
        pen.setJoinStyle(Qt.PenJoinStyle.RoundJoin)
        self.pen = pen

    def sizeHint(self):
        w = math.ceil(self.outlineThickness() * 2)
        return super().sizeHint() + QSize(w, w)

    def minimumSizeHint(self):
        w = math.ceil(self.outlineThickness() * 2)
        return super().minimumSizeHint() + QSize(w, w)

    def paintEvent(self, event):
        w = self.outlineThickness()
        rect = self.rect()
        metrics = QFontMetrics(self.font())
        tr = metrics.boundingRect(self.text()).adjusted(0, 0, w, w)
        if self.indent() == -1:
            if self.frameWidth():
                indent = (metrics.boundingRect('x').width() + w * 2) / 2
            else:
                indent = w
        else:
            indent = self.indent()

        if self.alignment() & Qt.AlignmentFlag.AlignLeft:
            x = rect.left() + indent - min(metrics.leftBearing(self.text()[0]), 0)
        elif self.alignment() & Qt.AlignmentFlag.AlignRight:
            x = rect.x() + rect.width() - indent - tr.width()
        else:
            x = (rect.width() - tr.width()) / 2

        if self.alignment() & Qt.AlignmentFlag.AlignTop:
            y = rect.top() + indent + metrics.ascent()
        elif self.alignment() & Qt.AlignmentFlag.AlignBottom:
            y = rect.y() + rect.height() - indent - metrics.descent()
        else:
            y = (rect.height() + metrics.ascent() - metrics.descent()) / 2

        path = QPainterPath()
        path.addText(x, y, self.font(), self.text())
        qp = QPainter(self)
        qp.setRenderHint(QPainter.RenderHint.Antialiasing)

        self.pen.setWidthF(w * 2)
        qp.fillPath(path, self.palette().window())
        qp.fillPath(path, self.brush)

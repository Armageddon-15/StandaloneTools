from PyQt6.QtWidgets import QLabel, QPushButton, QMenu, QWidget, QGridLayout, QVBoxLayout, QFrame, QHBoxLayout, QFileDialog
from PyQt6.QtWidgets import QSizePolicy, QSpinBox, QAbstractSpinBox, QApplication, QLineEdit, QComboBox, QScrollArea
from PyQt6.QtGui import QFont, QIcon, QImage, QPixmap, QDrag, QPalette, QColor
from PyQt6.QtCore import Qt, QSize, QRect, QThread, QPoint, QMimeData, QByteArray
from PyQt6 import QtCore

from image_utils import *
from CR_enum import *
from Drag_and_Drop_Overlay import DnDWidget
from IO_Item import ImportImage, ExportImage

import sys
import Recomp
import GUI_Settings


class Window(QWidget):
    def __init__(self):
        super(Window, self).__init__()
        self.setMinimumSize(int(GUI_Settings.picture_size*5), int(GUI_Settings.picture_size*2))

        self.importer_count = 1
        self.exporter_count = 1
        self.importers = [ImportImage(self, "", 1)]
        self.exporters = [ExportImage(self)]

        self.import_scroll = QScrollArea(self)
        self.import_widget = QWidget(self.import_scroll)
        self.import_scroll.setFrameStyle(0)
        # self.import_scroll.setRollingStep(120)
        self.import_scroll.setWidgetResizable(True)
        self.import_vbox = QVBoxLayout(self.import_widget)
        self.setContentsMargins(0, 0, 0, 0)
        self.import_vbox.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
        self.import_scroll_vbox = QVBoxLayout(self.import_scroll)
        self.import_scroll_vbox.setSpacing(0)
        self.import_scroll_vbox.setContentsMargins(0, 0, 0, 0)
        self.import_scroll_vbox.addWidget(self.import_widget)
        self.import_scroll.setWidget(self.import_widget)

        size_po = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        size_po.setVerticalStretch(1)

        self.import_stretch_frame = QFrame(self)
        self.import_stretch_frame.setSizePolicy(size_po)

        self.import_frame = QFrame(self)
        self.add_importer_btn = QPushButton(self)
        self.add_importer_btn.setText("Add")
        self.add_importer_btn.clicked.connect(self.addImporter)

        self.import_frame_vbox = QVBoxLayout(self.import_frame)
        self.import_frame_vbox.addWidget(self.import_scroll)
        self.import_frame_vbox.addWidget(self.add_importer_btn)

        self.separate_frame = QFrame(self)
        self.separate_frame.setFrameShape(QFrame.Shape.VLine)
        self.separate_frame.palette().setColor(QPalette.ColorRole.ToolTipText, QColor(25, 25, 25))

        self.export_scroll = QScrollArea(self)
        self.export_widget = QWidget(self.export_scroll)
        self.export_scroll.setFrameStyle(0)
        # self.export_scroll.setRollingStep(120)
        self.export_scroll.setWidgetResizable(True)
        self.export_vbox = QVBoxLayout(self.export_widget)
        self.export_vbox.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
        self.export_scroll_vbox = QVBoxLayout(self.export_scroll)
        self.export_scroll_vbox.setSpacing(0)
        self.export_scroll_vbox.setContentsMargins(0, 0, 0, 0)
        self.export_scroll_vbox.addWidget(self.export_widget)
        self.export_scroll.setWidget(self.export_widget)

        self.export_stretch_frame = QFrame(self)
        self.export_stretch_frame.setSizePolicy(size_po)

        self.export_frame = QFrame(self)
        self.add_exporter_btn = QPushButton(self)
        self.add_exporter_btn.setText("Add")
        self.add_exporter_btn.clicked.connect(self.addExporter)

        self.export_frame_vbox = QVBoxLayout(self.export_frame)
        self.export_frame_vbox.addWidget(self.export_scroll)
        self.export_frame_vbox.addWidget(self.add_exporter_btn)

        self.hbox = QHBoxLayout(self)
        self.hbox.addWidget(self.import_frame)
        self.hbox.addWidget(self.separate_frame)
        self.hbox.addWidget(self.export_frame)

        self.reLayoutImporters()
        self.reLayoutExporters()

    def reLayoutImporters(self):
        for i in reversed(range(0, self.import_vbox.count())):
            self.import_vbox.removeWidget(self.import_vbox.itemAt(i).widget())

        for imp in self.importers:
            self.import_vbox.addWidget(imp)

        self.import_vbox.addWidget(self.import_stretch_frame)

    def reLayoutExporters(self):
        for i in reversed(range(0, self.export_vbox.count())):
            self.export_vbox.removeWidget(self.export_vbox.itemAt(i).widget())

        for exp in self.exporters:
            self.export_vbox.addWidget(exp)

        self.export_vbox.addWidget(self.export_stretch_frame)

    def addImporter(self):
        filename = openReadOnlyFileDialog()
        if filename is not None:
            self.importer_count += 1
            importer = ImportImage(self, filename, self.importer_count)
            self.importers.append(importer)

            self.import_vbox.removeWidget(self.import_vbox.itemAt(self.import_vbox.count()-1).widget())
            self.import_vbox.addWidget(importer)
            self.import_vbox.addWidget(self.import_stretch_frame)

    def addExporter(self):
        exporter = ExportImage(self)
        self.exporters.append(exporter)

        self.export_vbox.removeWidget(self.export_vbox.itemAt(self.export_vbox.count() - 1).widget())
        self.export_vbox.addWidget(exporter)
        self.export_vbox.addWidget(self.export_stretch_frame)

    def findImageByIndex(self, index):
        for importer in self.importers:
            if importer.index == index:
                return importer.image_viewer

    def refreshConnectedViewer(self, index):
        iimg = Recomp.getImageByIndex(index)
        for link in iimg.linkers:
            if link is not None:
                link.refresh()

        for exp in self.exporters:
            exp.refresh()


def openReadOnlyFileDialog():
    dialog = QFileDialog()
    dialog.setFileMode(QFileDialog.FileMode.ExistingFile)
    dialog.setNameFilters(["All(*)", "Picture (*.jpg)", "Picture (*.png)", "Picture (*.tga)", "Picture (*.webp)"])
    dialog.setDirectory(os.path.abspath("../"))
    if dialog.exec():
        file_path = dialog.selectedFiles()[0]
        return file_path


if __name__ == '__main__':
    app = QApplication([])
    window = Window()
    window.show()
    sys.exit(app.exec())

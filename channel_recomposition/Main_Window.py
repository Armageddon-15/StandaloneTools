"""
Create By Armageddon15
Contact Me:
    github: https://github.com/Armageddon-15
    bilibili: https://space.bilibili.com/34445745
    email: hjc014@126.com
           bbb.hjc014@gmail.com

"""

from PyQt6.QtWidgets import QPushButton, QWidget, QVBoxLayout, QFrame, QHBoxLayout, QToolBar, QMainWindow
from PyQt6.QtWidgets import QSizePolicy, QApplication, QScrollArea
from PyQt6.QtGui import QPalette, QColor, QAction
from PyQt6.QtCore import QMimeData
from PyQt6 import QtCore

from QtUtil import *
from Drag_and_Drop_Overlay import StretchedDnD
from IO_Item import ImportImage, ExportImage
from Settings_GUI import PASettingWidget

import sys
import Recomp
import Settings_Classes


class Window(QWidget):
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)
        self.setMin()

        self.importer_count = 0
        self.exporter_count = 0
        self.importers = []
        self.exporters = []

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

        size_po = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        size_po.setVerticalStretch(1)

        self.import_stretch_frame = StretchedDnD(self)
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

        self.import_stretch_frame.update.connect(self.getMimeData)

    def setMin(self):
        self.setMinimumSize(int(Settings_Classes.detail_setting.picture_size*2 + Settings_Classes.detail_setting.half_picture_size*4 + 200),
                            int(max(Settings_Classes.detail_setting.picture_size, Settings_Classes.detail_setting.half_picture_size*2) + 200))

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

    def addImportFromFilename(self, filename):
        self.importer_count += 1
        importer = ImportImage(self, filename, self.importer_count)
        self.importers.append(importer)

        self.import_vbox.removeWidget(self.import_vbox.itemAt(self.import_vbox.count() - 1).widget())
        self.import_vbox.addWidget(importer)
        self.import_vbox.addWidget(self.import_stretch_frame)

    def addImporter(self):
        filename = openReadOnlyFileDialog()
        if filename is not None:
            self.addImportFromFilename(filename)

    def deleteImporter(self, obj):
        self.importers.remove(obj)

    def addExporter(self):
        exporter = ExportImage(self)
        self.exporters.append(exporter)

        self.export_vbox.removeWidget(self.export_vbox.itemAt(self.export_vbox.count() - 1).widget())
        self.export_vbox.addWidget(exporter)
        self.export_vbox.addWidget(self.export_stretch_frame)

    def deleteExporter(self, obj):
        self.exporters.remove(obj)

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

    def updateGui(self):
        self.setMin()
        for im in self.importers:
            im.updateGui()
        for ex in self.exporters:
            ex.updateGui()

    def getMimeData(self, data: QMimeData):
        file_path = data.text()
        if file_path.find(r"file:///") != -1:
            file_path = file_path.replace(r"file:///", "")
            file_paths = file_path.split("\n")
            try:
                file_paths.remove("")
            except ValueError:
                pass
            # filename = file_paths[len(file_paths)-1]
            for filename in file_paths:
                if not os.path.isdir(filename):
                    if os.path.splitext(filename)[1] in Recomp.support_format_set:
                        self.addImportFromFilename(filename)


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle("Channel Recompositor")
        self.setWindowSize()
        tool_bar = QToolBar(self)
        tool_bar.setMovable(False)
        self.addToolBar(tool_bar)

        setting_button = QAction("Settings", self)
        setting_button.triggered.connect(self.settingsClicked)
        tool_bar.addAction(setting_button)

        self.widget = Window(self)
        self.setCentralWidget(self.widget)

        self.setting_widget = PASettingWidget(self)

    def setWindowSize(self):
        if Settings_Classes.win_setting.use_this.getValue():
            widget_width = Settings_Classes.win_setting.width.value
            widget_height = Settings_Classes.win_setting.height.value
            widget_x = Settings_Classes.win_setting.x.value
            widget_y = Settings_Classes.win_setting.y.value
            self.setGeometry(widget_x, widget_y, widget_width, widget_height)

    def saveGeoPosition(self):
        if Settings_Classes.win_setting.use_this.getValue():
            geo = self.geometry()
            Settings_Classes.win_setting.setGeo(geo.x(), geo.y(), geo.width(), geo.height())
            Settings_Classes.saveAndLoad()

    def settingsClicked(self):
        self.setting_widget.setGeometry(self.x(), self.y(), self.setting_widget.sizeHint().width(), self.setting_widget.sizeHint().height())
        self.setting_widget.show()

    def runtimeUpdate(self):
        self.saveGeoPosition()
        self.widget.updateGui()

    def close(self) -> bool:
        print("s")
        self.setting_widget.close()
        super().close()
        return True

    def closeEvent(self, e) -> None:
        self.saveGeoPosition()
        super().closeEvent(e)

    def resizeEvent(self, e) -> None:
        self.saveGeoPosition()

    def resize(self, a0: QtCore.QSize) -> None:
        self.saveGeoPosition()


if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

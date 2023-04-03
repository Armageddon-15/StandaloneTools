from PyQt6.QtWidgets import QPushButton, QWidget, QGridLayout, QVBoxLayout, QFrame, QHBoxLayout, QDialog
from PyQt6.QtWidgets import QSizePolicy, QLineEdit
from PyQt6.QtCore import QRect, QMimeData

from QtUtil import *
from CR_Enum import *
from Drag_and_Drop_Overlay import DnDWidget
from viewer import ChannelViewer, ImageViewer
from Settings_GUI import PASettingWidget
from CustomDialog import CustomDialog

import copy
import Recomp
import Settings_Classes


class ImportImage(QWidget):
    def __init__(self, parent, path="", index=0):
        super(ImportImage, self).__init__(parent)
        self.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        self.setAcceptDrops(True)
        self.main = parent
        self.index = index
        self.filepath = path

        self.viewer_frame = QFrame(self)

        self.image_viewer = ImageViewer(self)
        ch_viewer_r = ChannelViewer(self, self.image_viewer, Channel.r)
        ch_viewer_g = ChannelViewer(self, self.image_viewer, Channel.g)
        ch_viewer_b = ChannelViewer(self, self.image_viewer, Channel.b)
        ch_viewer_a = ChannelViewer(self, self.image_viewer, Channel.a)
        self.chs = [ch_viewer_r, ch_viewer_g, ch_viewer_b, ch_viewer_a]

        self.ch_frame = QFrame(self)
        self.gbox = QGridLayout(self.ch_frame)
        self.gbox.setSpacing(2)
        self.gbox.setContentsMargins(0, 0, 0, 0)
        self.gbox.addWidget(ch_viewer_r, 0, 0)
        self.gbox.addWidget(ch_viewer_g, 0, 1)
        self.gbox.addWidget(ch_viewer_b, 1, 0)
        self.gbox.addWidget(ch_viewer_a, 1, 1)

        self.hbox = QHBoxLayout(self.viewer_frame)
        self.hbox.setContentsMargins(0, 0, 0, 0)
        self.hbox.addWidget(self.image_viewer)
        self.hbox.addWidget(self.ch_frame)

        self.operate_frame = QFrame(self)

        self.reimport_btn = QPushButton(self)
        self.reimport_btn.clicked.connect(self.reimportClicked)
        self.reimport_btn.setText("Reimport")

        self.delete_btn = QPushButton(self)
        self.delete_btn.clicked.connect(self.deleteClicked)
        self.delete_btn.setText("Delete")

        self.op_hbox = QHBoxLayout(self.operate_frame)
        self.op_hbox.setSpacing(0)
        self.op_hbox.addWidget(self.reimport_btn)
        self.op_hbox.addWidget(self.delete_btn)

        self.vbox = QVBoxLayout(self)
        self.vbox.setContentsMargins(0, 0, 0, 0)
        self.vbox.setSpacing(0)
        self.vbox.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.vbox.addWidget(self.viewer_frame)
        self.vbox.addWidget(self.operate_frame)

        self.dnd_check = DnDWidget(self)
        self.dnd_check.raise_()
        self.dnd_check.update.connect(self.getMimeData)
        self.dnd_check.setGeometry(QRect(0, 0, 0, 0))

        self.setImage(path)

    def setImage(self, path=""):
        if path != "":
            try:
                img = Image().readImage(path)
            except FileShouldBeEnglishOnly as e:
                dlg = CustomDialog()
                dlg.setWindowTitle("Warning")
                dlg.setText(e.reason)
                if dlg.exec():
                    print("Success!")
                else:
                    print("Cancel!")
            else:
                self.image_viewer.setImage(img)
                self.image_viewer.setFileName(path)
                if self.index in Recomp.import_images:
                    Recomp.import_images[self.index].update(img, self.image_viewer.name())
                else:
                    Recomp.import_images.update({self.index: Recomp.IndexedImage(img, self.image_viewer.name(), self.index)})

                for chv in self.chs:
                    chv.setImageFromMaster()

    def getMimeData(self, data: QMimeData):
        file_path = data.text()
        if file_path.find(r"file:///") != -1:
            file_path = file_path.replace(r"file:///", "")
            file_paths = file_path.split("\n")
            try:
                file_paths.remove("")
            except ValueError:
                pass
            filename = file_paths[len(file_paths)-1]
            if not os.path.isdir(filename):
                if os.path.splitext(filename)[1] in Recomp.support_format_set:
                    self.setImage(filename)
                    self.main.refreshConnectedViewer(self.index)

    def reimportClicked(self):
        filename = openReadOnlyFileDialog()
        if filename is not None:
            self.setImage(filename)

    def deleteClicked(self):
        iimg = Recomp.getImageByIndex(self.index)
        if iimg is not None:
            for link_ch_v in iimg.linkers:
                link_ch_v.clearSelf(remove=False)
            iimg.clearLinkers()
            Recomp.removeImageByIndex(self.index)
        self.image_viewer.deleteSelf()
        self.main.deleteImporter(self)
        self.deleteLater()

    def updateGui(self):
        img = None
        if self.filepath != "":
            try:
                img = Image().readImage(self.filepath)
            except FileShouldBeEnglishOnly as e:
                dlg = CustomDialog(self)
                dlg.setWindowTitle("Warning")
                dlg.setText(e.reason)
                if dlg.exec():
                    print("Success!")
                else:
                    print("Cancel!")
            else:
                self.image_viewer.updateGui(img)
        for ch_v in self.chs:
            ch_v.updateGui()

    def dragEnterEvent(self, e) -> None:
        self.dnd_check.setGeometry(0, 0, self.width(), self.height())

    def dragLeaveEvent(self, e) -> None:
        self.dnd_check.setGeometry(0, 0, 0, 0)


class ExportImage(QWidget):
    def __init__(self, parent, index=0):
        super(ExportImage, self).__init__(parent)
        self.main = parent
        self.index = index

        self.viewer_frame = QFrame(self)

        self.image_viewer = ImageViewer(self, is_getter=True)
        ch_viewer_r = ChannelViewer(self, self.image_viewer, Channel.r, is_getter=True)
        ch_viewer_g = ChannelViewer(self, self.image_viewer, Channel.g, is_getter=True)
        ch_viewer_b = ChannelViewer(self, self.image_viewer, Channel.b, is_getter=True)
        ch_viewer_a = ChannelViewer(self, self.image_viewer, Channel.a, is_getter=True)
        self.chs = [ch_viewer_r, ch_viewer_g, ch_viewer_b, ch_viewer_a]

        self.ch_frame = QFrame(self)
        self.gbox = QGridLayout(self.ch_frame)
        self.gbox.setSpacing(2)
        self.gbox.setContentsMargins(0, 0, 0, 0)
        self.gbox.addWidget(ch_viewer_r, 0, 0)
        self.gbox.addWidget(ch_viewer_g, 0, 1)
        self.gbox.addWidget(ch_viewer_b, 1, 0)
        self.gbox.addWidget(ch_viewer_a, 1, 1)

        self.hbox = QHBoxLayout(self.viewer_frame)
        self.hbox.setContentsMargins(0, 0, 0, 0)
        self.hbox.addWidget(self.ch_frame)
        self.hbox.addWidget(self.image_viewer)

        self.operate_frame = QFrame(self)

        size_po = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        size_po.setHorizontalStretch(1)
        self.path_line = QLineEdit(self)
        self.path_line.setSizePolicy(size_po)

        self.path_btn = QPushButton(self)
        self.path_btn.setMaximumSize(30, 30)
        self.path_btn.clicked.connect(self.pathBtnClicked)
        self.path_btn.setText("...")

        self.setting_btn = QPushButton(self)
        self.setting_btn.clicked.connect(self.setBtnClicked)
        self.setting_btn.setText("Settings")

        self.exp_btn = QPushButton(self)
        self.exp_btn.clicked.connect(self.exportBtnClick)
        self.exp_btn.setText("Export")

        self.delete_btn = QPushButton(self)
        self.delete_btn.setText("X")
        self.delete_btn.clicked.connect(self.deleteSelf)

        self.op_hbox = QHBoxLayout(self.operate_frame)
        self.op_hbox.setSpacing(0)
        self.op_hbox.addWidget(self.path_line)
        self.op_hbox.addWidget(self.path_btn)
        self.op_hbox.addWidget(self.setting_btn)
        self.op_hbox.addWidget(self.exp_btn)

        size_po = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        size_po.setVerticalStretch(1)
        self.viewer_frame.setSizePolicy(size_po)
        self.vbox = QVBoxLayout(self)
        self.vbox.setSpacing(0)
        self.vbox.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.vbox.setContentsMargins(0, 0, 0, 0)
        self.vbox.addWidget(self.viewer_frame)
        self.vbox.addWidget(self.operate_frame)

        self.exp_setting_widget = PASettingWidget(use_all_settings=False)
        self.exp_settings = copy.deepcopy(Settings_Classes.image_setting)
        self.path_line.setText(self.exp_settings.export_dir.getValue())
        self.exp_settings.export_dir.setValue("it will not be used here")
        self.exp_setting_widget.setImageSettingClass(self.exp_settings)

    def openWriteFileDialog(self):
        dialog = QFileDialog(self)
        dialog.setFileMode(QFileDialog.FileMode.Directory)
        dialog.setNameFilters(["All(*)"])
        dialog.setDirectory(os.path.abspath("../"))
        if dialog.exec():
            file_path = dialog.selectedFiles()[0]
            return file_path

    def pathBtnClicked(self):
        filepath = self.openWriteFileDialog()
        if filepath is not None:
            self.path_line.setText(filepath)

    def setBtnClicked(self):
        self.exp_setting_widget.show()

    def exportBtnClick(self):
        recomp = Recomp.Recompositer()
        for ch_v in self.image_viewer.ch_viewers:
            if ch_v.getter_ch != 0:
                recomp.setChannelImage(Recomp.getImageByIndex(ch_v.getter_index).image.getSingleChannel(ch_v.getter_ch), ch_v.ch)

        recomp.resize(self.exp_settings.res_x.getValue(), self.exp_settings.res_y.getValue(), Recomp.convertJsonStringToInterp(self.exp_settings.interpolation.getValue()))
        try:
            recomp.composite(self.path_line.text(), self.image_viewer.name(), self.exp_settings.format.getValue(),
                             Recomp.convertJsonStringToBit(self.exp_settings.bit.getValue()))
        except WrongChannelCount as e:
            dlg = CustomDialog(self)
            dlg.setWindowTitle("Warning")
            dlg.setText(e.reason)
            dlg.exec()
        except Exception as e:
            dlg = CustomDialog(self)
            dlg.setWindowTitle("Warning")
            dlg.setText(str(e))
            dlg.exec()
        else:
            if self.exp_settings.destroy_when_done.getValue():
                self.deleteSelf()

    def refresh(self):
        self.image_viewer.checkedRefresh()

    def deleteSelf(self):
        for ch_v in self.image_viewer.ch_viewers:
            ch_v.clearSelf()
        self.main.deleteExporter(self)

        self.deleteLater()

    def updateGui(self):
        self.image_viewer.updateGui(None)
        for ch_v in self.chs:
            ch_v.updateGui()

    def resizeEvent(self, e) -> None:
        self.delete_btn.setGeometry(self.width()-30, 0, 30, 30)


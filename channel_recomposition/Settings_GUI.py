from PyQt6.QtWidgets import QLabel, QPushButton, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QFrame, QCheckBox, QSpinBox
from PyQt6.QtWidgets import QSizePolicy, QApplication, QLineEdit, QFileDialog, QAbstractSpinBox, QRadioButton
from PyQt6.QtCore import Qt

from Recomp import support_format_dict

import sys
import Settings_Classes
import os


class SettingModify:
    def __init__(self, setting: Settings_Classes.SettingValue = None, **kwargs):
        self.is_setting_none = True
        if setting is not None:
            self.is_setting_none = False
        self.setting = setting

    def getValue(self):
        pass

    def setValue(self, v):
        pass

    def applyToSetting(self):
        if not self.is_setting_none:
            self.setting.setValue(self.getValue())

    def updateSetting(self):
        self.setValue(self.setting.getValue())


class PACheckBoxSetting(QFrame, SettingModify):
    def __init__(self, parent=None, name="Check Box", check=False, setting: Settings_Classes.SettingValue = None):
        super(PACheckBoxSetting, self).__init__(parent=parent, setting=setting)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        self.setSizePolicy(sizePolicy)

        self.check_box = QCheckBox(self)
        self.check_box.setText(name)
        # self.check_box.setStyleSheet("QCheckBox::indicator {border: 1px solid black; border-radius: 3px; }")

        if not self.is_setting_none:
            self.setValue(self.setting.getValue())
        else:
            self.setValue(check)

        self.stretch_frame = QFrame(self)
        self.hbox = QHBoxLayout(self)
        margins = 5
        self.hbox.setContentsMargins(15, margins, margins, margins)
        self.hbox.addWidget(self.check_box)
        self.hbox.addWidget(self.stretch_frame)

    def getValue(self):
        return self.check_box.isChecked()

    def setValue(self, check: bool):
        self.check_box.setChecked(check)


class PARadioButtonSetting(QFrame, SettingModify):
    def __init__(self, parent=None, name="Radio Group", default_option="Default", column_per_row=4, setting: Settings_Classes.SettingValue = None):
        super(PARadioButtonSetting, self).__init__(parent=parent, setting=setting)
        self.column_per_row = column_per_row
        self.name_label = QLabel(self)
        self.name_label.setText(name)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        self.name_label.setSizePolicy(sizePolicy)
        self.name_label.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.radios = [QRadioButton(self)]
        self.radios[0].setText(default_option)
        self.radios[0].setChecked(True)

        self.radio_frame = QFrame(self)
        # self.radio_frame.setStyleSheet("background-color: rgba(0,0,0,128)")
        self.radio_gbox = QGridLayout(self.radio_frame)
        self.radio_gbox.setContentsMargins(0, 0, 0, 0)
        self.radio_gbox.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
        self.radio_gbox.addWidget(self.radios[0], 0, 0)

        self.stretch_frame = QFrame(self)

        margins = 5
        self.hbox = QHBoxLayout(self)
        self.hbox.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.hbox.setContentsMargins(15, margins, margins, margins)
        self.hbox.addWidget(self.name_label)
        self.hbox.addWidget(self.stretch_frame)
        self.hbox.addWidget(self.radio_frame)

    def addRadioBox(self, option_name: str):
        cur_row = len(self.radios) // self.column_per_row
        cur_column = len(self.radios) % self.column_per_row
        if cur_column >= self.column_per_row:
            cur_row += 1
            cur_column = 0

        r = QRadioButton(self)
        r.setText(option_name)
        self.radios.append(r)
        self.radio_gbox.addWidget(r, cur_row, cur_column)
        cur_column += 1

    def addRadioBoxes(self, optional_names: list):
        cur_row = len(self.radios) // self.column_per_row
        cur_column = len(self.radios) % self.column_per_row
        for name in optional_names:
            if cur_column >= self.column_per_row:
                cur_row += 1
                cur_column = 0

            r = QRadioButton(self)
            r.setText(name)
            self.radios.append(r)
            self.radio_gbox.addWidget(r, cur_row, cur_column)
            cur_column += 1

    def updateValue(self):
        if not self.is_setting_none:
            self.setValue(self.setting.getValue())

    def getValue(self):
        for r in self.radios:
            if r.isChecked():
                return r.text()

    def setValue(self, v):
        for r in self.radios:
            r.setChecked(False)
            if r.text() == v:
                r.setChecked(True)


class PASpinBoxSetting(QFrame, SettingModify):
    def __init__(self, parent=None, name="Spin Box", value=0, max_value=999, min_va=0, setting: Settings_Classes.SettingValue = None):
        super(PASpinBoxSetting, self).__init__(parent=parent, setting=setting)
        self.name_label = QLabel(self)
        self.name_label.setText(name)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        self.name_label.setSizePolicy(sizePolicy)

        self.spinbox = QSpinBox(self)
        self.setMaxValue(max_value)
        self.setMinValue(min_va)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        self.spinbox.setSizePolicy(sizePolicy)
        self.spinbox.setStyleSheet(open("SpinBox.qss").read())
        self.spinbox.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)

        if not self.is_setting_none:
            self.updateSetting()
        else:
            self.setValue(value)

        self.stretch_frame = QFrame(self)

        self.hbox = QHBoxLayout(self)
        margins = 5
        self.hbox.setContentsMargins(15, margins, margins, margins)
        self.hbox.addWidget(self.name_label)
        self.hbox.addWidget(self.stretch_frame)
        self.hbox.addWidget(self.spinbox)

    def getValue(self):
        return self.spinbox.value()

    def setValue(self, v: int):
        self.spinbox.setValue(v)

    def setMaxValue(self, v: int):
        self.spinbox.setMaximum(v)

    def setMinValue(self, v: int):
        self.spinbox.setMinimum(v)


class PAFileSetting(QFrame, SettingModify):
    def __init__(self, parent=None, name="path", setting: Settings_Classes.SettingValue = None):
        super(PAFileSetting, self).__init__(parent=parent, setting=setting)
        self.name_label = QLabel(self)
        self.name_label.setText(name)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        self.name_label.setSizePolicy(sizePolicy)

        self.path_line = QLineEdit(self)
        self.path_line.setMinimumSize(250, 0)
        self.path_line.setStyleSheet("border-radius: 2px;border: 1px solid black;")

        if not self.is_setting_none:
            self.updateSetting()
        else:
            self.setValue("")

        self.read_file_btn = QPushButton(self)
        self.read_file_btn.setText("...")
        self.read_file_btn.setMinimumSize(25, 0)
        self.read_file_btn.setStyleSheet("border-radius: 2px;border: 1px solid black;")
        self.read_file_btn.clicked.connect(self.btnClicked)

        self.stretch_frame = QFrame(self)
        self.hbox = QHBoxLayout(self)
        margins = 5
        self.hbox.setContentsMargins(15, margins, margins, margins)
        self.hbox.addWidget(self.name_label)
        self.hbox.addWidget(self.stretch_frame)
        self.hbox.addWidget(self.path_line)
        self.hbox.addWidget(self.read_file_btn)

    def btnClicked(self):
        dialog = QFileDialog(self)
        dialog.setFileMode(QFileDialog.FileMode.Directory)
        dialog.setNameFilters(["All(*)"])
        dialog.setDirectory(os.path.abspath("../"))
        if dialog.exec():
            file_path = dialog.selectedFiles()[0]
            try:
                file_path = os.path.relpath(file_path)
            except ValueError:
                pass
            self.setValue(file_path)

    def getValue(self):
        return self.path_line.text()

    def setValue(self, s: str):
        self.path_line.setText(s)


class PASettingClassFrame(QFrame):
    def __init__(self, parent=None, name="Settings"):
        super(PASettingClassFrame, self).__init__(parent)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        self.setSizePolicy(sizePolicy)

        self.name_label = QLabel(self)
        self.name_label.setText(name)

        self.vbox = QVBoxLayout(self)
        self.vbox.setSpacing(0)
        self.vbox.addWidget(self.name_label)

        self.setting_frames = []

    def layoutSettingFrames(self):
        for setting_frame in self.setting_frames:
            self.vbox.addWidget(setting_frame)

    def addSettingFrame(self, setting_frame):
        self.setting_frames.append(setting_frame)
        self.vbox.addWidget(setting_frame)

    def applyToSettings(self):
        for setting_frame in self.setting_frames:
            setting_frame.applyToSetting()

    def updateSettings(self):
        for setting_frame in self.setting_frames:
            setting_frame.updateSetting()

    def length(self):
        return len(self.setting_frames)


class PASettingFrame(QFrame):
    def __init__(self, parent=None, *args, **kwargs):
        super(PASettingFrame, self).__init__(parent)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        self.setSizePolicy(sizePolicy)
        self.setStyleSheet("background-color: rgb(255, 255, 255);")

        self.setting_classes = []
        self.stretch_frame = QFrame(self)
        # self.stretch_frame.setStyleSheet("background-color: rgb(0, 255, 255);")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        self.stretch_frame.setSizePolicy(sizePolicy)
        self.vboxs = []
        self.hbox = QHBoxLayout(self)
        self.setSettings()
        self.layoutSettings()

    def setSettings(self):
        res_setting_class = PASettingClassFrame(self, "Resolution Setting:")
        res_setting_class.addSettingFrame(PACheckBoxSetting(self, "Remember last closed size", setting=Settings_Classes.win_setting.use_this))
        self.setting_classes.append(res_setting_class)

        detail_setting_class = PASettingClassFrame(self, "Detail Settings:")
        detail_setting_class.addSettingFrame(PASpinBoxSetting(self, "Big Picture size", setting=Settings_Classes.detail_setting.picture_size))
        detail_setting_class.addSettingFrame(PASpinBoxSetting(self, "Small Picture size", setting=Settings_Classes.detail_setting.half_picture_size))
        detail_setting_class.addSettingFrame(PASpinBoxSetting(self, "Title font size:", setting=Settings_Classes.detail_setting.font_size))
        detail_setting_class.addSettingFrame(PASpinBoxSetting(self, "Second Title font size", setting=Settings_Classes.detail_setting.half_font_size))
        self.setting_classes.append(detail_setting_class)

    def layoutSettings(self):
        i = 0
        vbox = QVBoxLayout()
        for s_class in self.setting_classes:
            if i % 2 == 0 or s_class.length() >= 10:
                vbox = QVBoxLayout()
                self.vboxs.append(vbox)
            else:
                i += 1
            s_class.layoutSettingFrames()
            vbox.addWidget(s_class)
            i += 1

        for box in self.vboxs:
            box.addWidget(QFrame(self))
            self.hbox.addLayout(box)

        self.hbox.addWidget(self.stretch_frame)

    def applyAllSettings(self):
        for s_class in self.setting_classes:
            s_class.applyToSettings()

    def updateAllSettings(self):
        for s_class in self.setting_classes:
            s_class.updateSettings()


class ImageSettingFrame(PASettingFrame):
    def __init__(self, parent=None, use_super=False, *args, **kwargs):
        self.setting = Settings_Classes.image_setting
        self.use_super = use_super
        self.set = False
        if self.use_super:
            self.set = True
        super(ImageSettingFrame, self).__init__(parent, *args, **kwargs)

    def setSettingClass(self, image_setting: Settings_Classes.ImageFormat = Settings_Classes.image_setting):
        self.setting = image_setting
        self.set = True
        self.setSettings()
        self.layoutSettings()

    def setSettings(self):
        if self.use_super:
            super().setSettings()

        if self.set:
            image_setting_class = PASettingClassFrame(self, "Image Settings")
            image_setting_class.addSettingFrame(PACheckBoxSetting(self, "Remove panel when export finish", setting=self.setting.destroy_when_done))
            image_setting_class.addSettingFrame(PASpinBoxSetting(self, "Resolution X", max_value=99999, setting=self.setting.res_x))
            image_setting_class.addSettingFrame(PASpinBoxSetting(self, "Resolution Y", max_value=99999, setting=self.setting.res_y))
            image_setting_class.addSettingFrame(PAFileSetting(self, "Export dir", setting=self.setting.export_dir))
            keys = []
            for key in support_format_dict.keys():
                keys.append(key)

            radio = PARadioButtonSetting(self, "Image Format", keys[0], 3, setting=self.setting.format)
            radio.addRadioBoxes(keys[1:])
            radio.updateValue()
            image_setting_class.addSettingFrame(radio)
            radio = PARadioButtonSetting(self, "Image Bit", "8", setting=self.setting.bit)
            radio.addRadioBoxes(["16", "32"])
            radio.updateValue()
            image_setting_class.addSettingFrame(radio)
            radio = PARadioButtonSetting(self, "Image Filter", "nearest", 3, setting=self.setting.interpolation)
            radio.addRadioBoxes(["linear", "cubic", "lanczos4"])
            radio.updateValue()
            image_setting_class.addSettingFrame(radio)
            self.setting_classes.append(image_setting_class)


class PASettingWidget(QWidget):
    def __init__(self, window=None, setting_frame=ImageSettingFrame, use_all_settings=True, title="Settings"):
        super(PASettingWidget, self).__init__()
        self.setWindowTitle(title)
        self.main = window
        self.use_all = use_all_settings

        self.setting_frame = setting_frame(self, use_all_settings)
        self.btn_frame = QFrame(self)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        self.btn_frame.setSizePolicy(sizePolicy)
        self.stretch_frame = QFrame(self.btn_frame)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        self.stretch_frame.setSizePolicy(sizePolicy)
        self.apply_btn = QPushButton(self.btn_frame)
        self.apply_btn.setText("Apply")
        self.apply_btn.clicked.connect(self.applyBtnClicked)

        self.accept_btn = QPushButton(self.btn_frame)
        self.accept_btn.setText("Accept")
        self.accept_btn.clicked.connect(self.acceptBtnClicked)

        self.cancel_btn = QPushButton(self.btn_frame)
        self.cancel_btn.setText("Cancel")
        self.cancel_btn.clicked.connect(self.cancelBtnClicked)

        self.btn_hbox = QHBoxLayout(self.btn_frame)
        self.btn_hbox.addWidget(self.stretch_frame)
        self.btn_hbox.addWidget(self.apply_btn)
        self.btn_hbox.addWidget(self.accept_btn)
        self.btn_hbox.addWidget(self.cancel_btn)

        self.vbox = QVBoxLayout(self)
        self.vbox.addWidget(self.setting_frame)
        self.vbox.addWidget(self.btn_frame)

    def setImageSettingClass(self, setting_class: Settings_Classes.ImageFormat):
        if type(self.setting_frame) is ImageSettingFrame:
            self.setting_frame.setSettingClass(setting_class)

    def applyBtnClicked(self):
        self.setting_frame.applyAllSettings()
        if self.use_all:
            Settings_Classes.saveAndLoad()
        self.setting_frame.updateAllSettings()
        if self.main is not None:
            self.main.runtimeUpdate()

    def acceptBtnClicked(self):
        self.applyBtnClicked()
        self.close()

    def cancelBtnClicked(self):
        self.close()


def main():
    app = QApplication([])
    window = PASettingWidget(use_all_settings=True)
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()

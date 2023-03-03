from PyQt6 import QtWidgets
import sys


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Hello World")
        l = QtWidgets.QLabel("My simple app.")
        l.setMargin(10)
        self.setCentralWidget(l)
        self.show()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    app.exec()


"""
use this line to build application:
venv\Scripts\pyinstaller.exe main.py

build tutorial:
https://www.pythonguis.com/tutorials/packaging-pyqt6-applications-windows-pyinstaller/

"""
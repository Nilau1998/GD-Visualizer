import os
from PyQt5 import QtWidgets, uic

ui_file = os.path.join("gui", "resources", "main_window.ui")
Ui_MainWindow, _ = uic.loadUiType(ui_file)


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
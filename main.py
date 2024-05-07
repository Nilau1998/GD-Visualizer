from gui.main_window import MainWindow

from PyQt5 import QtWidgets
import sys


if "__main__" == __name__:
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
from gui.weight_visualizer_widget import WeightVisualizerWidget
from gui.main_window_logic import MainWindowLogic
from gui.gd_visualizer_widget import GDVisualizerWidget

import os
import time
from PyQt5 import QtWidgets, uic
from PyQt5.QtGui import QIntValidator

ui_file = os.path.join("gui", "resources", "main_window.ui")
Ui_MainWindow, _ = uic.loadUiType(ui_file)


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)

        # QLineEdit Validator
        self.epochs_lineedit.setValidator(QIntValidator())

        # Model visualizer widget
        self.weight_visualizer = WeightVisualizerWidget()
        self.weight_visualizer_scroll_area = QtWidgets.QScrollArea()
        self.weight_visualizer_scroll_area.setWidget(self.weight_visualizer)
        self.weight_visualizer_widget.setLayout(QtWidgets.QVBoxLayout())
        self.weight_visualizer_widget.layout().addWidget(self.weight_visualizer)

        # Model GD visualizer
        self.gd_visualizer = GDVisualizerWidget()
        self.gd_visualizer_widget.setLayout(QtWidgets.QVBoxLayout())
        self.gd_visualizer_widget.layout().addWidget(self.gd_visualizer)

        # Logic
        self.logic = MainWindowLogic(self, self.weight_visualizer, self.gd_visualizer)

        # Signals
        self.model_selection_combobox.currentIndexChanged.connect(self.logic.handle_model_selection)
        self.forward_button.clicked.connect(self.logic.handle_forward_button)
        self.epochs_lineedit.returnPressed.connect(self.logic.handle_epochs_entered)
        self.finish_training_button.clicked.connect(self.logic.handle_finish_training_button)

    def resizeEvent(self, event):
        self.weight_visualizer.update()
        super(MainWindow, self).resizeEvent(event)

    def toggle_training_buttons(self, state):
        self.forward_button.setEnabled(state)
        self.backward_button.setEnabled(state)
        self.finish_training_button.setEnabled(state)
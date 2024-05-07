from gui.model_visualizer_widget import ModelVisualizer
from models.logistic_regression import LogisticRegression

import os
import time
from PyQt5 import QtWidgets, uic
from PyQt5.QtGui import QIntValidator
from PyQt5.QtCore import QThread, pyqtSignal

ui_file = os.path.join("gui", "resources", "main_window.ui")
Ui_MainWindow, _ = uic.loadUiType(ui_file)

class ProgressBarThread(QThread):
    progress = pyqtSignal(int)

    def __init__(self):
        QThread.__init__(self)
        self.avg_time = 0

    def run(self):
        start = time.time()
        while time.time() - start < self.avg_time:
            print("now")
            result = int(((time.time() - start) / self.avg_time) * 100)
            self.progress.emit(result)


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)

        # Progress bar
        self.progress_bar_thread = ProgressBarThread()
        self.recorded_times = []
        self.avg_time = 0

        # QLineEdit Validator
        self.epochs_lineedit.setValidator(QIntValidator())

        # Model visualizer widget
        self.model_visualizer = ModelVisualizer()
        self.model_visualizer_scroll_area = QtWidgets.QScrollArea()
        self.model_visualizer_scroll_area.setWidget(self.model_visualizer)
        self.weight_visualizer_widget.setLayout(QtWidgets.QVBoxLayout())
        self.weight_visualizer_widget.layout().addWidget(self.model_visualizer)

        # Init values
        self.model_visualizer.logic.set_model(
                    LogisticRegression(
                        alpha=float(self.alpha_lineedit.text()),
                        eta0=float(self.eta0_lineedit.text()
                        )
                    )
                )

        # Signals
        self.model_selection_combobox.currentIndexChanged.connect(self.handle_model_selection)
        self.forward_button.clicked.connect(self.handle_forward_button)
        self.epochs_lineedit.returnPressed.connect(self.handle_epochs_entered)
        self.progress_bar_thread.progress.connect(self.update_training_progress_bar)

    def handle_model_selection(self, index):
        selected_value = self.model_selection_combobox.currentText()
        match selected_value:
            case "Logistic Regression":
                self.model_visualizer.logic.set_model(
                    LogisticRegression(
                        alpha=float(self.alpha_lineedit.text()),
                        eta0=float(self.eta0_lineedit.text()
                        )
                    )
                )
            case "Simple Neural Network":
                print("Simple Neural Network model is not implemented yet")

    def handle_forward_button(self):
        start_time = time.time()
        self.progress_bar_thread.avg_time = self.avg_time
        self.progress_bar_thread.start()
        w, b, log_loss_train, log_loss_test = self.model_visualizer.logic.model.train_step()
        end_time = time.time()
        self.training_time_label.setText(f"Training time: {end_time - start_time:.2f} seconds")
        self.recorded_times.append(end_time - start_time)
        self.avg_time = sum(self.recorded_times) / len(self.recorded_times)

        self.model_visualizer.update_weights(w)

    def handle_epochs_entered(self):
        epoch = int(self.epochs_lineedit.text())
        self.epochs_lineedit.clearFocus()
        valid_epoch_count = epoch > 0
        self.forward_button.setEnabled(valid_epoch_count)
        self.backward_button.setEnabled(valid_epoch_count)

    def update_training_progress_bar(self, value):
        self.training_progress_bar.setValue(value)

    def resizeEvent(self, event):
        self.model_visualizer.update()
        super(MainWindow, self).resizeEvent(event)
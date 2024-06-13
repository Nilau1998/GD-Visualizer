from models.logistic_regression import LogisticRegression
from utils.thread_pool import ThreadPool
from concurrent.futures import ThreadPoolExecutor

from PyQt5.QtCore import QObject, QThread, pyqtSignal
import time

class TrainingThread(QThread):
    def __init__(self, parent=None):
        super(TrainingThread, self).__init__(parent)
        self.main_window_logic = parent

    def run(self):
        epochs = int(self.main_window_logic.main_window_ui.epochs_lineedit.text()) - self.main_window_logic.model_visualizer_ui.logic.model.current_epoch
        with ThreadPoolExecutor(max_workers=1) as executor:
            for _ in range(epochs):
                future = executor.submit(self.main_window_logic._training_loop)
                future.result()

class MainWindowLogic(QObject):
    toggle_training_buttons_signal = pyqtSignal(bool)
    toggle_foward_button_signal = pyqtSignal(bool)
    update_weights_signal = pyqtSignal(object)
    update_current_epoch_signal = pyqtSignal(str)

    def __init__(self, main_window_ui, model_visualizer_ui):
        super().__init__()
        self.main_window_ui = main_window_ui
        self.model_visualizer_ui = model_visualizer_ui

        self.thread_pool = ThreadPool(8)

        self.toggle_training_buttons_signal.connect(self.main_window_ui.toggle_training_buttons)
        self.toggle_foward_button_signal.connect(self.main_window_ui.forward_button.setEnabled)
        self.update_weights_signal.connect(self.model_visualizer_ui.update_weights)
        self.update_current_epoch_signal.connect(self.main_window_ui.current_epoch_label.setText)

        # Init
        self.handle_model_selection()

    def set_model_visualizer(self, model_visualizer):
        self.model_visualizer_ui = model_visualizer

    def handle_model_selection(self):
        selected_value = self.main_window_ui.model_selection_combobox.currentText()
        match selected_value:
            case "Logistic Regression":
                self.model_visualizer_ui.logic.set_model(
                    LogisticRegression(
                        alpha=float(self.main_window_ui.alpha_lineedit.text()),
                        eta0=float(self.main_window_ui.eta0_lineedit.text()
                        )
                    )
                )
            case "Simple Neural Network":
                print("Simple Neural Network model is not implemented yet")

    def handle_forward_button(self):
        self.toggle_training_buttons_signal.emit(False)
        self.thread_pool.submit(self.__training_loop)

    def handle_finish_training_button(self):
        self.toggle_training_buttons_signal.emit(False)
        self.training_thread = TrainingThread(self)
        self.training_thread.start()

    def _training_loop(self):
        start_time = time.time()
        w, b, log_loss_train, log_loss_test = self.model_visualizer_ui.logic.model.train_step()
        end_time = time.time()
        self.main_window_ui.training_time_label.setText(f"Training time: {end_time - start_time:.2f} seconds")
        self.update_weights_signal.emit(w)
        self.toggle_training_buttons_signal.emit(True)
        self.update_current_epoch_label(self.model_visualizer_ui.logic.model.current_epoch)
        if self.model_visualizer_ui.logic.model.current_epoch >= int(self.main_window_ui.epochs_lineedit.text()):
            self.toggle_foward_button_signal.emit(False)

    def update_current_epoch_label(self, epoch):
        result = f"Current epoch: {epoch}"
        self.update_current_epoch_signal.emit(result)


    def handle_epochs_entered(self):
        epoch = int(self.main_window_ui.epochs_lineedit.text())
        self.main_window_ui.epochs_lineedit.clearFocus()
        valid_epoch_count = epoch > 0
        self.toggle_training_buttons_signal.emit(valid_epoch_count)
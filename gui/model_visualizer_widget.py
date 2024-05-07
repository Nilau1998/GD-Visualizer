from gui.model_visualizer_logic import ModelVisualizerLogic

from PyQt5 import QtWidgets
from PyQt5.QtGui import QPainter

class ModelVisualizer(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super(ModelVisualizer, self).__init__(*args, **kwargs)

        self.logic = ModelVisualizerLogic(
            self.width(),
            self.height()
        )

    def update_weights(self, weights):
        self.logic.update_weights(weights)
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        self.logic.draw(painter)

    def resizeEvent(self, event):
        self.logic.window_width = self.width()
        self.logic.window_height = self.height()
        self.logic.construct_model()
        self.update()

        super(ModelVisualizer, self).resizeEvent(event)
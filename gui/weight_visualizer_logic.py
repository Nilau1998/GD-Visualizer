from models.logistic_regression import LogisticRegression

from PyQt5.QtGui import QBrush, QPen, QColor, QFont
from PyQt5.QtCore import Qt, QRect

class WeightVisualizerLogic:
    def __init__(self, window_width, window_height):
        self.model = None
        self.window_width = window_width
        self.window_height = window_height
        self.padding = 30
        self.node_radius = window_width * 0.02

        self.nodes = []
        self.edges = []

        self.last_weights = None

    def draw(self, painter):
        for node in self.nodes:
            node.draw(painter)

        for edge in self.edges:
            edge.draw(painter)

    def set_model(self, model):
        self.model = model
        self.construct_model()


    def construct_model(self):
        self.nodes = []
        self.edges = []

        self.node_radius = self.window_width * 0.02

        if isinstance(self.model, LogisticRegression):
            self.__construct_logistic_regression_model()

    def __construct_logistic_regression_model(self):
        model_architecture = self.model.get_model_architecture()

        space_between_nodes = (self.window_width) / model_architecture["layer1"]
        for i in range(model_architecture["layer1"]):
            self.nodes.append(Node(self.padding + space_between_nodes * i, self.window_height / 2, self.node_radius, QColor(150, 150, 150)))

    def update_weights(self, weights):
        if self.last_weights is not None:
            diff = self.last_weights = weights
            for i, weight in enumerate(weights):
                self.nodes[i].value = weight
                if diff[i] > 0:
                    self.nodes[i].color = QColor(0, 255, 0)
                else:
                    self.nodes[i].color = QColor(255, 0, 0)
        else:
            self.last_weights = weights
            for i, weight in enumerate(weights):
                self.nodes[i].value = weight
                if weight > 0:
                    self.nodes[i].color = QColor(0, 255, 0)
                else:
                    self.nodes[i].color = QColor(255, 0, 0)



class Node:
    def __init__(self, x, y, radius, color):
        self.x = int(x)
        self.y = int(y)
        self.radius = int(radius)
        self.color = color
        self.value = 0

    def draw(self, painter):
        painter.setBrush(QBrush(self.color))
        painter.drawEllipse(self.x, self.y, self.radius, self.radius)

        if self.value is not None:
            painter.save()
            painter.setPen(QPen(Qt.black))
            painter.setFont(QFont("Arial", 8))
            painter.drawText(QRect(self.x, self.y, self.radius, self.radius), Qt.AlignCenter, str(round(self.value, 2)))
            painter.restore()

class Edge:
    def __init__(self, start_node, end_node, color):
        self.start_node = start_node
        self.end_node = end_node
        self.color = color

    def draw(self, painter):
        pen = QPen()
        pen.setColor(self.color)
        painter.setPen(pen)
        painter.drawLine(self.start_node.x, self.start_node.y, self.end_node.x, self.end_node.y)
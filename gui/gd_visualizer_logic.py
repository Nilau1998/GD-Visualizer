import numpy as np
import matplotlib.pyplot as plt

class GDVisualizerLogic:
    def __init__(self, canvas):
        self.canvas = canvas
        self.plot()

    def plot(self):
        # Generate X and Y values
        x = np.linspace(-5, 5, 100)
        y = np.linspace(-5, 5, 100)
        X, Y = np.meshgrid(x, y)

        # Calculate Z values
        Z = self.z_function(X, Y)

        # Create a 3D subplot
        ax = self.canvas.figure.add_subplot(111, projection='3d')

        # Plot the surface
        ax.plot_surface(X, Y, Z, cmap='viridis')

        # Redraw the canvas
        self.canvas.draw()

    def z_function(self, x, y):
        return np.sin(np.sqrt(x ** 2 + y ** 2))
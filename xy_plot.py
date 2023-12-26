import sys
import numpy as np
import pyqtgraph as pg
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout

class XYPlot(QWidget):
    def __init__(self):
        super().__init__()

        plt = pg.plot()
        

        # Number of points
        n = 300

        # Generate random data for the XY plot
        x_data = np.linspace(0, 1, n)
        y_data = np.random.normal(loc=0, scale=1e-5, size=n) # np.sin(2 * np.pi * x_data)

        # Create a PlotCurveItem for the XY plot
        line1 = plt.plot(x_data, y_data, pen ='g', symbol ='x', symbolPen ='g',
						symbolBrush = 0.2, name ='green')

        layout = QGridLayout()
        self.setLayout(layout)
        layout.addWidget(plt, 0, 1, 3, 1)
        

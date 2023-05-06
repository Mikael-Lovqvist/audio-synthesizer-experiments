# pip install --user QCustomPlot2
# pacman -S qcustomplot

import sys

from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPen, QBrush, QColor
from PyQt5.QtWidgets import QApplication, QMainWindow
from QCustomPlot2 import *

def plot_buffer(buffer, sample_rate):


	app = QApplication(sys.argv)
	window = QMainWindow()
	window.resize(800, 600)

	customPlot = QCustomPlot()

	customPlot.setBackground(QColor(20, 20, 20))

	window.setCentralWidget(customPlot)

	customPlot.xAxis.grid().setPen(QPen(QColor(0, 100, 0), 1, Qt.DotLine))
	customPlot.yAxis.grid().setPen(QPen(QColor(0, 100, 0), 1, Qt.DotLine))

	customPlot.xAxis.setBasePen(QPen(QColor(200, 100, 0), 1, Qt.SolidLine))
	customPlot.yAxis.setBasePen(QPen(QColor(200, 100, 0), 1, Qt.SolidLine))

	customPlot.xAxis.grid().setZeroLinePen(QPen(QColor(0, 200, 0), 1, Qt.SolidLine))
	customPlot.yAxis.grid().setZeroLinePen(QPen(QColor(0, 200, 0), 1, Qt.SolidLine))

	customPlot.xAxis.setTickPen(QPen(QColor(250, 255, 200), 1, Qt.SolidLine))
	customPlot.yAxis.setTickPen(QPen(QColor(250, 255, 200), 1, Qt.SolidLine))

	customPlot.xAxis.setSubTickPen(QPen(QColor(150, 155, 100), 1, Qt.SolidLine))
	customPlot.yAxis.setSubTickPen(QPen(QColor(150, 155, 100), 1, Qt.SolidLine))

	customPlot.xAxis.setTickLabelColor(QColor(50, 255, 150))
	customPlot.yAxis.setTickLabelColor(QColor(50, 255, 150))


	graph = customPlot.addGraph()
	graph.setPen(QPen(QColor(150, 50, 255)))
	graph.setBrush(QBrush(QColor(100, 100, 255, 20)))


	customPlot.setInteraction(QCP.iRangeDrag)
	customPlot.setInteraction(QCP.iRangeZoom)
	customPlot.setInteraction(QCP.iSelectPlottables)

	x, y = [], []

	for i, v in enumerate(buffer):	#100 ms
		t = i / sample_rate
		x.append(t)
		y.append(v)

	graph.setData(x, y)
	customPlot.replot()
	customPlot.rescaleAxes()

	window.show()
	sys.exit(app.exec_())

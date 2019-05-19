import sys

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtChart import *


class MonitorWidget(QWidget):
    def __init__(self, *args, **kwargs):
        super(MonitorWidget, self).__init__(*args, **kwargs)

        self.vbox = QVBoxLayout()

        self.setStyleSheet('QWidget{background-color:rgb(56, 59, 64)}')

        chart = QChart()
        chart.setTitle("Line Chart 1")
        series = QLineSeries()
        series.append(0, 6)
        series.append(2, 4)
        chart.addSeries(series)
        chart.createDefaultAxes()


        chart.setBackgroundBrush(QBrush(QColor(56, 59, 64), Qt.SolidPattern))
        chart.setPlotAreaBackgroundVisible(True)
        chart.setPlotAreaBackgroundBrush(QBrush(QColor("#4caf50"), Qt.SolidPattern))
        chart.setTheme(1)

        view = QChartView(chart)
        view.setRenderHint(QPainter.Antialiasing)

        self.vbox.addWidget(view)
        self.setLayout(self.vbox)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    obj = MonitorWidget()
    obj.show()
    sys.exit(app.exec_())
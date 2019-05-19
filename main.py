import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from ControlWidget import ControlWidget
from TableWidget import TableWidget


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.resize(1624, 660)

        controlWidget = ControlWidget()
        monitorWidget = TableWidget()

        splitter = QSplitter()
        splitter.addWidget(controlWidget)
        splitter.addWidget(monitorWidget)
        splitter.setStretchFactor(0, 6)
        splitter.setStretchFactor(1, 10)

        self.setCentralWidget(splitter)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    obj = MainWindow()
    obj.show()
    sys.exit(app.exec_())
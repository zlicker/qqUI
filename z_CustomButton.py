import sys

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class CustomButton(QPushButton):
    def __init__(self):
        super().__init__()
        self.setText('hello')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    obj = CustomButton()
    obj.show()
    sys.exit(app.exec_())
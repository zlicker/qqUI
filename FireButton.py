from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys

class FireButton(QPushButton):

    def __init__(self, *args, **kwargs):
        super(FireButton, self).__init__(*args, **kwargs)

        self.setCheckable(True)
        self.setFlat(True)
        self.setFixedSize(100, 100)
        #self.pressed.connect(self.changeIcon)
        self.setIcon(QIcon('./images/Bullet.png'))
        self.setIconSize(QSize(80, 80))
        self.setStyleSheet("QToolButton{border-style: flat;}")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    obj = FireButton()
    obj.show()
    sys.exit(app.exec_())

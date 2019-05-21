from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys

class PowerButton(QToolButton):
    state = None

    def __init__(self, *args, **kwargs):
        super(PowerButton, self).__init__(*args, **kwargs)

        self.setCheckable(True)
        #self.setFlat(True)
        self.setFixedSize(100, 100)
        self.pressed.connect(self.changeIcon)
        self.setIcon(QIcon('./images/Power_Off.png'))
        self.setIconSize(QSize(100, 100))
        self.setStyleSheet("QToolButton{border-style: flat;}")
        #self.setStyleSheet("QPushButton{border-image: url(./images/Lock_lock.png);}")
        self.state = False

    def changeIcon(self):
        if self.isChecked():
            self.setIcon(QIcon('./images/Power_Off.png'))
            self.setIconSize(QSize(100, 100))
            #self.setStyleSheet("QPushButton{border-image: url(./images/Lock_lock.png);}")
            self.state = False
        else:
            self.setIcon(QIcon('./images/Power_Up.png'))
            self.setIconSize(QSize(100, 100))
            #self.setStyleSheet("QPushButton{border-image: url(./images/Open_lock.png);}")
            self.state = True


    #######################################################################################
    #def enterEvent(self, QEvent):
    #    self.setStyleSheet("QPushButton{border-image: url(./images/Open_lock.png);}")
    #
    #def mousePressEvent(self, QEvent):
    #    if self.isChecked():
    #        self.setStyleSheet("QPushButton{border-image: url(./images/Lock_lock.png);}")
    #        print('h')
    #    else:
    #        self.setStyleSheet("QPushButton{border-image: url(./images/Open_lock.png);}")
    #        print('h')
    #######################################################################################


if __name__ == '__main__':
    app = QApplication(sys.argv)
    obj = PowerButton()
    obj.show()
    sys.exit(app.exec_())

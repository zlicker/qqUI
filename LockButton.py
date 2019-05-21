from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys

class LockButton(QToolButton):
    lock = None

    def __init__(self, *args, **kwargs):
        super(LockButton, self).__init__(*args, **kwargs)

        self.setCheckable(True)
        #self.setFlat(True)
        self.setFixedSize(100, 100)
        self.pressed.connect(self.changeIcon)
        self.setIcon(QIcon('./images/Lock_lock.png'))
        self.setIconSize(QSize(100, 100))
        self.setStyleSheet("QToolButton{border-style: flat;}")
        self.lock = True

    def changeIcon(self):
        if self.isChecked():
            self.setIcon(QIcon('./images/Lock_lock.png'))
            self.setIconSize(QSize(100, 100))
            #self.setStyleSheet("QPushButton{border-image: url(./images/Lock_lock.png);}")
            self.lock = True
        else:
            self.setIcon(QIcon('./images/Open_lock.png'))
            self.setIconSize(QSize(100, 100))
            #self.setStyleSheet("QPushButton{border-image: url(./images/Open_lock.png);}")
            self.lock = False


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
    obj = LockButton()
    obj.show()
    sys.exit(app.exec_())

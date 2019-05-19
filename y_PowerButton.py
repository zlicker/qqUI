import sys
import time

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class PowerButton(QPushButton):
    def __init__(self, *args, **kwargs):
        super(PowerButton, self).__init__(*args, **kwargs)
        self.resize(100, 100)
        self.setStyleSheet("QPushButton{border-image: url(./qqUI/CustomButton/images/power-button02.png);}")
        #self.setStyleSheet("QPushButton{background-color:rgb(56, 59, 64);}")
        #self.setMask(QRegion(QRect(5, 5, 90, 90), QRegion.Ellipse))
        self.setMask(QRegion(QRect(0, 0, 100, 100), QRegion.Ellipse))

        self.status = 0

        #self.clicked.connect(self.showc)
        self.pressed.connect(self.showc)
        self.released.connect(self.rec)

    def showc(self):
        while self.status == 0:
            #QApplication.processEvents()
            time.sleep(0.3)
            print('hello')
    
    def rec(self):
        self.status = 1


    #def paintEvent(self, QPaintEvent):
    #    self.painter = QPainter()
    #    self.painter.begin(self)
    #    self.paint()
    #    self.painter.end()

    #def paint(self):
    #    #self.painter.drawRect(250, 15, 90, 60)
    #    #self.painter.drawArc(QRectF(100, 100, 200, 200), 30*16, 120*16)
    #    self.painter.setPen(QPen(QColor('#f44336')))
    #    self.painter.setBrush(QBrush(QColor("#FFCDD2")))
    #    self.painter.drawPie(QRectF(0, 0, 100, 100), 30*16, 120*16)

    #def mousePressEvent(self, QMouseEvent):
    #    print('hello')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    obj = PowerButton()
    obj.show()
    app.exec_()
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys

class VelocitySlider(QSlider):
    velocity = 0

    def __init__(self, *args, **kwargs):
        super(VelocitySlider, self).__init__(*args, **kwargs)
        self.setMinimum(1)
        self.setMaximum(100)

        #self.setStyleFunc()
        def setStyleFunc(self):
            self.setStyleSheet("""
                QSlider{
                    border-color: #bcbcbc;
                }
                QSlider::groove:vertical{
                    border: 1px solid #999999;
                    width: 20px;
                    margin: 0px 0;
                    left: 5px;
                    right: 5px;

                }
                QSlider::handle:Vertical{
                    height: 13px
                    width: 13px;
                    border-image: url(./images/dragHandle.png);
                    margin: -7px -7px -7px -7px;
                }

                """)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    obj = VelocitySlider()
    obj.show()
    sys.exit(app.exec_())

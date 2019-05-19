#! /home/zlicker/anaconda3/bin/python
import sys
#import RPi.GPIO as GPIO
#sys.path.append('./qqUI/CustomButton/')

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from LockButton import LockButton
from PowerButton import PowerButton
from FireButton import FireButton

class ControlWidget(QWidget):
    times = 0

    def __init__(self, *args, **kwargs):
        super(ControlWidget, self).__init__(*args, **kwargs)

        self.mainGridLayout = QGridLayout()
        self.setLayout(self.mainGridLayout)
        self.resize(700, 400)

        #self.initGPIO()
        self.initButtons()

        self.createLayout()

    def initButtons(self):
        #! init Direction Buttons *******************************************
        self.upButton = QPushButton('')
        self.downButton = QPushButton('')
        self.leftButton = QPushButton('')
        self.rightButton = QPushButton('')


        self.upButton.pressed.connect(self.upButtonPressed)
        self.downButton.pressed.connect(self.downButtonPressed)
        self.leftButton.pressed.connect(self.leftButtonPressed)
        self.rightButton.pressed.connect(self.rightButtonPressed)

        imagePath = './images/'

        self.upButton.setIcon(QIcon(imagePath+'up.png'))
        self.leftButton.setIcon(QIcon(imagePath+'left.png'))
        self.rightButton.setIcon(QIcon(imagePath+'right.png'))
        self.downButton.setIcon(QIcon(imagePath+'down.png'))

        for pb in (self.upButton, self.leftButton, self.rightButton, self.downButton):
            self.setButtonProperty(pb)
            
        #! Initialize Lock Button *******************************************
        self.lockButton = LockButton()

        #! Initialize Power Button ******************************************
        self.powerButton = PowerButton()
        self.powerButton.pressed.connect(self.powerButtonPressed)

        #! Initialize Fire Button *******************************************
        self.fireButton = FireButton()
        self.fireButton.pressed.connect(self.fireButtonPressed)
        self.fireButton.released.connect(self.fireButtonReleased)

    def setButtonProperty(self, pb=QPushButton):
        iconXSize = 100
        iconYSize = 100
        buttonXSize = 100
        buttonYSize = 100

        #pb.setCheckable(True)
        pb.setFlat(True)
        pb.setStyleSheet("QToolButton{border-style: flat;}")
        pb.setIconSize(QSize(iconXSize, iconYSize))
        pb.setFixedSize(buttonXSize, buttonYSize)
        pb.setAutoRepeat(True)
        pb.setAutoRepeatInterval(1e-3)
        
    def createLayout(self):
        self.mainGridLayout.addWidget(self.upButton, 0, 1)
        self.mainGridLayout.addWidget(self.leftButton, 1, 0)
        self.mainGridLayout.addWidget(self.rightButton, 1, 2)
        self.mainGridLayout.addWidget(self.downButton, 2, 1)

        self.mainGridLayout.addWidget(self.lockButton, 1, 1)

        self.mainGridLayout.addWidget(self.powerButton, 3, 0)
        self.mainGridLayout.addWidget(self.fireButton, 3, 2)

    def upButtonPressed(self):
        if self.lockButton.lock == False:
            GPIO.output(self.servo_1_dir_neg, GPIO.HIGH)
            GPIO.output(self.servo_1_step_neg, GPIO.HIGH)
            GPIO.output(self.servo_1_step_neg, GPIO.LOW)

    def downButtonPressed(self):
        if self.lockButton.lock == False:
            GPIO.output(self.servo_1_dir_neg, GPIO.LOW)
            GPIO.output(self.servo_1_step_neg, GPIO.HIGH)
            GPIO.output(self.servo_1_step_neg, GPIO.LOW)

    def leftButtonPressed(self):
        if self.lockButton.lock == False:
            GPIO.output(self.servo_2_dir_neg, GPIO.HIGH)
            GPIO.output(self.servo_2_step_neg, GPIO.HIGH)
            GPIO.output(self.servo_2_step_neg, GPIO.LOW)

    def rightButtonPressed(self):
        if self.lockButton.lock == False:
            GPIO.output(self.servo_2_dir_neg, GPIO.LOW)
            GPIO.output(self.servo_2_step_neg, GPIO.HIGH)
            GPIO.output(self.servo_2_step_neg, GPIO.LOW)

    def powerButtonPressed(self):
        buttonState = self.powerButton.state
        if buttonState == True:
            GPIO.output(self.power_id, GPIO.HIGH)
        elif buttonState == False:
            GPIO.output(self.power_id, GPIO.LOW)

    def fireButtonPressed(self):
        GPIO.output(self.relay_id, GPIO.HIGH)

    def fireButtonReleased(self):
        GPIO.output(self.relay_id, GPIO.LOW)


    def initGPIO(self):
        self.servo_1_step_neg = 2
        self.servo_1_dir_neg = 3
        self.servo_2_step_neg = 17
        self.servo_2_dir_neg = 27

        self.power_id = 10
        self.relay_id = 9

        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)

        GPIO.setup(self.servo_1_step_neg, GPIO.OUT)
        GPIO.setup(self.servo_1_dir_neg, GPIO.OUT)
        GPIO.setup(self.servo_2_step_neg, GPIO.OUT)
        GPIO.setup(self.servo_2_dir_neg, GPIO.OUT)
        GPIO.setup(self.power_id, GPIO.OUT)
        GPIO.setup(self.relay_id, GPIO.OUT)

        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    obj = ControlWidget()
    obj.show()
    sys.exit(app.exec_())

    ########################################################
    #def pbReleased(self):
    #    if self.lockButton.lock == False:
    #        print('Released\t', self.times)
    #        self.times += 1

    #def pbClicked(self):
    #    if self.lockButton.lock == False:
    #        print('Clicked\t', self.times)
    #        self.times += 1
    ########################################################
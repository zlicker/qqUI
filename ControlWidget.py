import sys
#import RPi.GPIO as GPIO
import time
from threading import Thread

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from LockButton import LockButton
from PowerButton import PowerButton
from FireButton import FireButton
from VelocitySlider import VelocitySlider

class ControlWidget(QWidget):
    times = 0

    def __init__(self, *args, **kwargs):
        super(ControlWidget, self).__init__(*args, **kwargs)

        self.mainGridLayout = QGridLayout()
        self.setLayout(self.mainGridLayout)
        self.resize(600, 400)

        #self.initGPIO()
        self.initButtons()

        t = Thread(target=self.runMotor)
        t.start()

        self.createLayout()

    def initButtons(self):
        #! init Direction Buttons *******************************************
        self.upButton = QPushButton('')
        self.downButton = QPushButton('')
        self.leftButton = QPushButton('')
        self.rightButton = QPushButton('')


        #self.upButton.pressed.connect(self.upButtonPressed)
        #self.downButton.pressed.connect(self.downButtonPressed)
        #self.leftButton.pressed.connect(self.leftButtonPressed)
        #self.rightButton.pressed.connect(self.rightButtonPressed)

        imagePath = './images/'

        self.upButton.setIcon(QIcon(imagePath+'up.png'))
        self.leftButton.setIcon(QIcon(imagePath+'left.png'))
        self.rightButton.setIcon(QIcon(imagePath+'right.png'))
        self.downButton.setIcon(QIcon(imagePath+'down.png'))

        for pb in (self.upButton, self.leftButton,
        self.rightButton, self.downButton):
            self.setButtonProperty(pb)

        #! Initialize the Velocity Slider ***********************************
        self.verticalVelSlider = VelocitySlider()
        self.horziontalVelSlider = VelocitySlider()
        self.verticalVelSlider.valueChanged.connect(self.verticalVelChanged)
        self.horziontalVelSlider.valueChanged.connect(self.horizontalVelChanged)
            
        #! Initialize Lock Button *******************************************
        self.lockButton = LockButton()
        self.lockButton.clicked.connect(self.lockButtonPressed)

        #! Initialize Power Button ******************************************
        self.powerButton = PowerButton()
        self.powerButton.pressed.connect(self.powerButtonPressed)

        #! Initialize Fire Button *******************************************
        self.fireButton = FireButton()
        self.fireButton.pressed.connect(self.fireButtonPressed)
        self.fireButton.released.connect(self.fireButtonReleased)

        # Disable other buttons.
        self.lockButtonPressed()

    def setButtonProperty(self, pb):
        iconXSize = 100
        iconYSize = 100
        buttonXSize = 100
        buttonYSize = 100

        #pb.setCheckable(True)
        pb.setFlat(True)
        #pb.setStyleSheet("QToolButton{border-style: flat;}")
        pb.setIconSize(QSize(iconXSize, iconYSize))
        pb.setFixedSize(buttonXSize, buttonYSize)
        #pb.setAutoRepeat(True)
        #pb.setAutoRepeatInterval(1)
        
    def createLayout(self):
        self.mainGridLayout.addWidget(self.verticalVelSlider, 0, 0, 3, 1, Qt.AlignHCenter)
        self.mainGridLayout.addWidget(self.horziontalVelSlider, 0, 4, 3, 1, Qt.AlignHCenter)

        self.mainGridLayout.addWidget(self.upButton, 0, 2)
        self.mainGridLayout.addWidget(self.leftButton, 1, 1)
        self.mainGridLayout.addWidget(self.rightButton, 1, 3)
        self.mainGridLayout.addWidget(self.downButton, 2, 2)

        self.mainGridLayout.addWidget(self.lockButton, 1, 2)

        self.mainGridLayout.addWidget(self.powerButton, 3, 1, 1, 2)
        self.mainGridLayout.addWidget(self.fireButton, 3, 3, 1, 2)

    def runMotor(self):
        while True:
            if self.upButton.isDown():
                GPIO.setup(self.servo_1_dir_neg, 0)
                GPIO.setup(self.servo_1_step_neg, 1)
                time.sleep(1e-3)
                GPIO.setup(self.servo_1_step_neg, 0)
            elif self.downButton.isDown():
                GPIO.setup(self.servo_1_dir_neg, 1)
                GPIO.setup(self.servo_1_step_neg, 1)
                time.sleep(1)
                GPIO.setup(self.servo_1_step_neg, 0)
            elif self.leftButton.isDown():
                GPIO.setup(self.servo_2_dir_neg, 1)
                GPIO.setup(self.servo_2_step_neg, 1)
                time.sleep(1e-3)
                GPIO.setup(self.servo_2_step_neg, 0)
            elif self.rightButton.isDown():
                GPIO.setup(self.servo_2_dir_neg, 0)
                GPIO.setup(self.servo_2_step_neg, 1)
                time.sleep(1e-3)
                GPIO.setup(self.servo_2_step_neg, 0)


    def lockButtonPressed(self):
        if self.lockButton.lock == True:
            self.upButton.setEnabled(False)
            self.downButton.setEnabled(False)
            self.leftButton.setEnabled(False)
            self.rightButton.setEnabled(False)
            self.fireButton.setEnabled(False)
        elif self.lockButton.lock == False:
            self.upButton.setEnabled(True)
            self.downButton.setEnabled(True)
            self.leftButton.setEnabled(True)
            self.rightButton.setEnabled(True)
            self.fireButton.setEnabled(True)

    def upButtonPressed(self):
        GPIO.setup(self.servo_1_dir_neg, 1)
        GPIO.setup(self.servo_1_step_neg, 1)
        #time.sleep(5e-3)
        GPIO.setup(self.servo_1_step_neg, 0)

    def downButtonPressed(self):
        GPIO.setup(self.servo_1_dir_neg, GPIO.LOW)
        GPIO.setup(self.servo_1_step_neg, GPIO.HIGH)
        #time.sleep(self.verticalVelocity)
        GPIO.setup(self.servo_1_step_neg, GPIO.LOW)

    def leftButtonPressed(self):
        GPIO.setup(self.servo_2_dir_neg, GPIO.HIGH)
        GPIO.setup(self.servo_2_step_neg, GPIO.HIGH)
        time.sleep(1e-3)
        #time.sleep(self.horizontalVelocity)
        GPIO.setup(self.servo_2_step_neg, GPIO.LOW)

    def rightButtonPressed(self):
        GPIO.setup(self.servo_2_dir_neg, GPIO.LOW)
        GPIO.setup(self.servo_2_step_neg, GPIO.HIGH)
        #time.sleep(self.horizontalVelocity)
        GPIO.setup(self.servo_2_step_neg, GPIO.LOW)

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

    def verticalVelChanged(self):
        self.verticalVelocity = 1 / self.verticalVelSlider.value()
        #self.upButton.setAutoRepeatInterval(self.verticalVelocity)
        #self.downButton.setAutoRepeatInterval(self.verticalVelocity)

    def horizontalVelChanged(self):
        self.horizontalVelocity = 1 / self.horziontalVelSlider.value()
        #self.leftButton.setAutoRepeatInterval(self.horizontalVelocity)
        #self.rightButton.setAutoRepeatInterval(self.horizontalVelocity)

    def initGPIO(self):
        self.servo_1_step_neg = 2	
        self.servo_1_dir_neg = 3
        self.servo_2_step_neg = 17
        self.servo_2_dir_neg = 27

        self.power_id = 10
        self.relay_id = 9

        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(True)

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

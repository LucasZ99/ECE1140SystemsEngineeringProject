import sys
import os
from PyQt6 import uic
from PyQt6.QtWidgets import (QMainWindow, QApplication, QPushButton, QLineEdit, QCheckBox)

from Train_Model import TrainModel
from trainControllerTot_Container import TrainController_Tot_Container


class TrainPhysicsCalculator(QMainWindow):

    def __init__(self):
        super(TrainPhysicsCalculator, self).__init__()
        self.train = TrainModel(TrainController_Tot_Container())
        self.train.crew.mass_per_person = 0

        # load the ui file
        current_dir = os.path.dirname(__file__)  # setting up to work in any dir
        ui_path = os.path.join(current_dir, 'train_physics_calculator.ui')
        try:
            uic.loadUi(ui_path, self)
        except Exception as e:
            print("Error with loading UI file: ", e)

        # buttons
        self.button = self.findChild(QPushButton, "button")
        self.button.clicked.connect(self.button_pushed)

        # line edits
        self.power = self.findChild(QLineEdit, "power")
        self.acceleration = self.findChild(QLineEdit, "acceleration")
        self.velocity = self.findChild(QLineEdit, "velocity")
        self.mass = self.findChild(QLineEdit, "mass")
        self.grade = self.findChild(QLineEdit, "grade")
        self.time = self.findChild(QLineEdit, "time")

        # check boxes
        self.s_brake = self.findChild(QCheckBox, "s_brake")
        self.e_brake = self.findChild(QCheckBox, "e_brake")

        self.power.setText(str(self.train.engine.power))
        self.acceleration.setText(str(self.train.acceleration))
        self.velocity.setText(str(self.train.velocity))
        self.mass.setText(str(self.train.train_const.train_mass()))
        self.grade.setText(str(self.train.old_block.grade))
        self.time.setText("1")

        self.show()

    def button_pushed(self):
        self.train.engine.set_power(float(self.power.text()))
        self.train.acceleration = float(self.acceleration.text())
        self.train.velocity = float(self.velocity.text())
        self.train.train_const.mass_per_car = float(self.mass.text())
        self.train.old_block.grade = float(self.grade.text())
        self.train.brakes.service_brake = self.s_brake.isChecked()
        self.train.brakes.driver_ebrake = self.e_brake.isChecked()

        self.train.physics_calculation(float(self.time.text()))
        self.train.position = 0

        self.acceleration.setText(f'{self.train.acceleration: .2f}')
        self.velocity.setText(f"{self.train.velocity: .2f}")


app = QApplication(sys.argv)
ui = TrainPhysicsCalculator()
app.exec()

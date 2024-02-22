import sys
import train_model_object
from PyQt5 import uic
from PyQt5.QtWidgets import (QMainWindow, QApplication, QLabel, QPushButton, QGroupBox,
                             QCheckBox, QComboBox, QProgressBar, QLineEdit)
import random


class UITrain(QMainWindow):
    # constants
    tons_per_kilogram = 0.00110231
    feet_per_meter = 3.28084

    def __init__(self):
        super(UITrain, self).__init__()

        # load the ui file
        uic.loadUi("Train_Model_UI.ui", self)

        # declare the train object
        self.train = train_model_object.TrainModel()

        # define widgets
        self.physicsButton = self.findChild(QPushButton, "physicsButton")
        self.passengerButton = self.findChild(QPushButton, "passengerButton")

        self.primeGroup = self.findChild(QGroupBox, "primeGroup")
        self.trainSelect = self.findChild(QComboBox, "trainSelect")
        self.emerButton = self.findChild(QPushButton, "emerButton")
        self.tbCheck = self.findChild(QCheckBox, "tbCheck")

        self.phyGroup = self.findChild(QGroupBox, "phyGroup")
        self.powerValue = self.findChild(QLabel, "powerValue")
        self.accValue = self.findChild(QLabel, "accValue")
        self.speedValue = self.findChild(QLabel, "speedValue")
        self.totMassValue = self.findChild(QLabel, "totMassValue")
        self.gradeValue = self.findChild(QLabel, "gradeValue")
        self.elevValue = self.findChild(QLabel, "elevValue")
        self.pBrakeValue = self.findChild(QProgressBar, "pBrakeValue")
        self.sBrakeValue = self.findChild(QProgressBar, "sBrakeValue")
        self.dBrakeValue = self.findChild(QProgressBar, "dBrakeValue")

        self.trainGroup = self.findChild(QGroupBox, "trainGroup")
        self.lengthValue = self.findChild(QLabel, "lengthValue")
        self.heightValue = self.findChild(QLabel, "heightValue")
        self.widthValue = self.findChild(QLabel, "widthValue")
        self.carsValue = self.findChild(QLabel, "carsValue")
        self.trainMassValue = self.findChild(QLabel, "trainMassValue")
        self.crewValue = self.findChild(QLabel, "crewValue")
        self.passValue = self.findChild(QLabel, "passValue")

        self.failGroup = self.findChild(QGroupBox, "failGroup")
        self.eFailCheck = self.findChild(QCheckBox, "eFailCheck")
        self.sFailCheck = self.findChild(QCheckBox, "sFailCheck")
        self.bFailCheck = self.findChild(QCheckBox, "bFailCheck")

        self.transGroup = self.findChild(QGroupBox, "transGroup")
        self.recSpeedValue = self.findChild(QLabel, "recSpeedValue")
        self.authValue = self.findChild(QLabel, "authValue")
        self.beaconValue = self.findChild(QLabel, "beaconValue")

        self.opGroup = self.findChild(QGroupBox, "opGroup")
        self.tempValue = self.findChild(QLabel, "tempValue")
        self.extLightValue = self.findChild(QProgressBar, "extLightValue")
        self.intLightValue = self.findChild(QProgressBar, "intLightValue")
        self.leftDoorValue = self.findChild(QProgressBar, "leftDoorValue")
        self.rightDoorValue = self.findChild(QProgressBar, "rightDoorValue")

        self.phyGroup_tb = self.findChild(QGroupBox, "phyGroup_tb")
        self.powerValue_tb = self.findChild(QLineEdit, "powerTextBox")
        self.accValue_tb = self.findChild(QLineEdit, "accTextBox")
        self.speedValue_tb = self.findChild(QLineEdit, "speedTextBox")
        self.totMassValue_tb = self.findChild(QLineEdit, "totMassTextBox")
        self.gradeValue_tb = self.findChild(QLineEdit, "gradeTextBox")
        self.elevValue_tb = self.findChild(QLineEdit, "elevTextBox")
        self.pBrakeValue_tb = self.findChild(QCheckBox, "pBrakeCheck")
        self.sBrakeValue_tb = self.findChild(QCheckBox, "sBrakeCheck")
        self.dBrakeValue_tb = self.findChild(QCheckBox, "dBrakeCheck")

        self.trainGroup_tb = self.findChild(QGroupBox, "trainGroup_tb")
        self.lengthValue_tb = self.findChild(QLabel, "lengthValue_tb")
        self.heightValue_tb = self.findChild(QLabel, "heightValue_tb")
        self.widthValue_tb = self.findChild(QLabel, "widthValue_tb")
        self.carsValue_tb = self.findChild(QLineEdit, "carsTextBox")
        self.trainMassValue_tb = self.findChild(QLabel, "trainMassValue_tb")
        self.crewValue_tb = self.findChild(QLineEdit, "crewTextBox")
        self.passValue_tb = self.findChild(QLineEdit, "passTextBox")

        self.transGroup_tb = self.findChild(QGroupBox, "transGroup_tb")
        self.recSpeedValue_tb = self.findChild(QLineEdit, "recSpeedTextBox")
        self.authValue_tb = self.findChild(QLineEdit, "authTextBox")
        self.beaconValue_tb = self.findChild(QLineEdit, "beaconTextBox")

        self.opGroup_tb = self.findChild(QGroupBox, "opGroup_tb")
        self.tempValue_tb = self.findChild(QLineEdit, "tempTextBox")
        self.extLightValue_tb = self.findChild(QCheckBox, "extLightCheck")
        self.intLightValue_tb = self.findChild(QCheckBox, "intLightCheck")
        self.leftDoorValue_tb = self.findChild(QCheckBox, "leftDoorCheck")
        self.rightDoorValue_tb = self.findChild(QCheckBox, "rightDoorCheck")

        # populate values
        self.populate_values()

        # define behavior
        self.phyGroup_tb.hide()
        self.trainGroup_tb.hide()
        self.transGroup_tb.hide()
        self.opGroup_tb.hide()
        self.tb = False
        self.ebp = False

        self.physicsButton.pressed.connect(self.physics_test)
        self.passengerButton.pressed.connect(self.passenger_test)

        self.emerButton.pressed.connect(self.set_pbrake)
        self.tbCheck.stateChanged.connect(self.tb_toggle)
        self.powerValue_tb.editingFinished.connect(self.power_change)
        self.accValue_tb.editingFinished.connect(self.acc_change)
        self.speedValue_tb.editingFinished.connect(self.speed_change)
        self.totMassValue_tb.editingFinished.connect(self.tot_mass_change)
        self.gradeValue_tb.editingFinished.connect(self.grade_change)
        self.elevValue_tb.editingFinished.connect(self.elev_change)
        self.pBrakeValue_tb.stateChanged.connect(self.pbrake_change)
        self.sBrakeValue_tb.stateChanged.connect(self.sbrake_change)
        self.dBrakeValue_tb.stateChanged.connect(self.dbrake_change)
        self.carsValue_tb.editingFinished.connect(self.cars_change)
        self.crewValue_tb.editingFinished.connect(self.crew_change)
        self.passValue_tb.editingFinished.connect(self.pass_change)
        self.eFailCheck.stateChanged.connect(self.engine_change)
        self.sFailCheck.stateChanged.connect(self.signal_change)
        self.bFailCheck.stateChanged.connect(self.brake_change)
        self.recSpeedValue_tb.editingFinished.connect(self.rec_speed_changed)
        self.authValue_tb.editingFinished.connect(self.auth_changed)
        self.beaconValue_tb.editingFinished.connect(self.beacon_changed)
        self.tempValue_tb.editingFinished.connect(self.temp_change)
        self.extLightValue_tb.stateChanged.connect(self.ext_light_change)
        self.intLightValue_tb.stateChanged.connect(self.int_light_change)
        self.leftDoorValue_tb.stateChanged.connect(self.left_door_change)
        self.rightDoorValue_tb.stateChanged.connect(self.right_door_change)

        # show the app
        self.show()

    def tb_toggle(self):
        if self.tb:
            self.phyGroup.show()
            self.trainGroup.show()
            self.transGroup.show()
            self.opGroup.show()

            self.phyGroup_tb.hide()
            self.trainGroup_tb.hide()
            self.transGroup_tb.hide()
            self.opGroup_tb.hide()
            self.tb = False
        else:
            self.phyGroup.hide()
            self.trainGroup.hide()
            self.transGroup.hide()
            self.opGroup.hide()

            self.phyGroup_tb.show()
            self.trainGroup_tb.show()
            self.transGroup_tb.show()
            self.opGroup_tb.show()
            self.tb = True

    def physics_test(self):
        self.train.physics_calculation(1)
        self.populate_values()

    def passenger_test(self):
        self.train.station_passenger_update(random.randint(0, 50))
        self.populate_values()

    def set_pbrake(self):
        self.train.enable_passenger_emergency_brake()
        self.ebp = True
        self.populate_values()
        self.ebp = False

    def power_change(self):
        self.train.set_power(float(self.powerValue_tb.text()))
        self.populate_values()

    def acc_change(self):
        self.train.set_acceleration(float(self.accValue_tb.text()) * 5280 / self.feet_per_meter / 3600 / 3600)
        self.populate_values()

    def speed_change(self):
        self.train.set_velocity(float(self.speedValue_tb.text()) * 5280 / self.feet_per_meter / 3600)
        self.populate_values()

    def tot_mass_change(self):
        self.train.set_total_mass(float(self.totMassValue_tb.text()) / self.tons_per_kilogram)
        self.populate_values()

    def grade_change(self):
        self.train.set_grade(float(self.gradeValue_tb.text()))
        self.populate_values()

    def elev_change(self):
        self.train.set_elevation(float(self.elevValue_tb.text()) / self.feet_per_meter)
        self.populate_values()

    def pbrake_change(self):
        if not self.ebp:
            if self.train.get_passenger_emergency_brake():
                self.train.disable_passenger_emergency_brake()
            else:
                self.train.enable_passenger_emergency_brake()
            self.populate_values()
        self.ebp = False

    def sbrake_change(self):
        if self.train.get_service_brake():
            self.train.disable_service_brake()
        else:
            self.train.enable_service_brake()
        self.populate_values()

    def dbrake_change(self):
        if self.train.get_driver_emergency_brake():
            self.train.disable_driver_emergency_brake()
        else:
            self.train.enable_driver_emergency_brake()
        self.populate_values()

    def cars_change(self):
        self.train.set_car_count(int(self.carsValue_tb.text()))
        self.populate_values()

    def crew_change(self):
        self.train.set_crew_count(int(self.crewValue_tb.text()))
        self.populate_values()

    def pass_change(self):
        self.train.set_passenger_count(int(self.passValue_tb.text()))
        self.populate_values()

    def engine_change(self):
        if self.train.get_engine_failure():
            self.train.fix_engine()
        else:
            self.train.fail_engine()
        self.populate_values()

    def signal_change(self):
        if self.train.get_signal_pickup_failure():
            self.train.fix_signal_pickup()
        else:
            self.train.fail_signal_pickup()
        self.populate_values()

    def brake_change(self):
        if self.train.get_brake_failure():
            self.train.fix_brake()
        else:
            self.train.fail_brake()
        self.populate_values()

    def rec_speed_changed(self):
        self.train.set_commanded_velocity(int(self.recSpeedValue_tb.text()))
        self.populate_values()

    def auth_changed(self):
        self.train.set_authority(int(self.authValue_tb.text()))
        self.populate_values()

    def beacon_changed(self):
        self.train.set_beacon(self.beaconValue_tb.text())
        self.populate_values()

    def temp_change(self):
        self.train.set_interior_temp(int(self.tempValue_tb.text()))
        self.populate_values()

    def ext_light_change(self):
        if self.train.get_exterior_light():
            self.train.exterior_lights_off()
        else:
            self.train.exterior_lights_on()
        self.populate_values()

    def int_light_change(self):
        if self.train.get_interior_light():
            self.train.interior_lights_off()
        else:
            self.train.interior_lights_on()
        self.populate_values()

    def left_door_change(self):
        if self.train.get_left_door():
            self.train.left_door_close()
        else:
            self.train.left_door_open()
        self.populate_values()

    def right_door_change(self):
        if self.train.get_right_door():
            self.train.right_door_close()
        else:
            self.train.right_door_open()
        self.populate_values()

    def populate_values(self):
        self.powerValue.setText(f'{self.train.get_power(): .2f} W')
        self.powerValue_tb.setText(f'{self.train.get_power(): .2f}')
        self.accValue.setText(
            f"{self.train.get_acceleration() * self.feet_per_meter * 3600 * 3600 / 5280: .2f} mph<sup>2")
        self.accValue_tb.setText(f"{self.train.get_acceleration() * self.feet_per_meter * 3600 * 3600 / 5280: .2f}")
        self.speedValue.setText(f'{self.train.get_velocity() * self.feet_per_meter * 3600 / 5280: .2f} mph')
        self.speedValue_tb.setText(f'{self.train.get_velocity() * self.feet_per_meter * 3600 / 5280: .2f}')
        self.totMassValue.setText(f'{self.train.get_total_mass() * self.tons_per_kilogram: .2f} Tons')
        self.totMassValue_tb.setText(f'{self.train.get_total_mass() * self.tons_per_kilogram: .2f}')
        self.gradeValue.setText(f'{self.train.get_grade(): .2f} %')
        self.gradeValue_tb.setText(f'{self.train.get_grade(): .2f}')
        self.elevValue.setText(f'{self.train.get_elevation() * self.feet_per_meter: .2f} ft')
        self.elevValue_tb.setText(f'{self.train.get_elevation() * self.feet_per_meter: .2f}')
        if self.train.get_passenger_emergency_brake():
            self.pBrakeValue.setValue(100)
        else:
            self.pBrakeValue.setValue(0)
        self.pBrakeValue_tb.setChecked(self.train.get_passenger_emergency_brake())

        if self.train.get_service_brake():
            self.sBrakeValue.setValue(100)
        else:
            self.sBrakeValue.setValue(0)
        self.sBrakeValue_tb.setChecked(self.train.get_service_brake())

        if self.train.get_driver_emergency_brake():
            self.dBrakeValue.setValue(100)
        else:
            self.dBrakeValue.setValue(0)
        self.dBrakeValue_tb.setChecked(self.train.get_driver_emergency_brake())

        self.lengthValue.setText(f'{self.train.get_train_length() * self.feet_per_meter: .2f} ft')
        self.lengthValue_tb.setText(f'{self.train.get_train_length() * self.feet_per_meter: .2f} ft')
        self.heightValue.setText(f'{self.train.get_height() * self.feet_per_meter: .2f} ft')
        self.heightValue_tb.setText(f'{self.train.get_height() * self.feet_per_meter: .2f} ft')
        self.widthValue.setText(f'{self.train.get_width() * self.feet_per_meter: .2f} ft')
        self.widthValue_tb.setText(f'{self.train.get_width() * self.feet_per_meter: .2f} ft')
        self.carsValue.setText(f'{self.train.get_car_count()}')
        self.carsValue_tb.setText(f'{self.train.get_car_count()}')
        self.trainMassValue.setText(f'{self.train.get_train_mass() * self.tons_per_kilogram: .2f} Tons')
        self.trainMassValue_tb.setText(f'{self.train.get_train_mass() * self.tons_per_kilogram: .2f} Tons')
        self.crewValue.setText(f'{self.train.get_crew_count()}')
        self.crewValue_tb.setText(f'{self.train.get_crew_count()}')
        self.passValue.setText(f'{self.train.get_passenger_count()}')
        self.passValue_tb.setText(f'{self.train.get_passenger_count()}')

        self.eFailCheck.setChecked(self.train.get_engine_failure())
        self.sFailCheck.setChecked(self.train.get_signal_pickup_failure())
        self.bFailCheck.setChecked(self.train.get_brake_failure())

        self.recSpeedValue.setText(f'0x{self.train.get_commanded_velocity():02x}')
        self.recSpeedValue_tb.setText(f'{self.train.get_commanded_velocity():02x}')
        self.authValue.setText(f'0x{self.train.get_authority():02x}')
        self.authValue_tb.setText(f'{self.train.get_authority():02x}')
        self.beaconValue.setText(self.train.get_beacon())
        self.beaconValue_tb.setText(self.train.get_beacon())

        self.tempValue.setText(f'{self.train.get_interior_temp()} °F')
        self.tempValue_tb.setText(f'{self.train.get_interior_temp()}')

        if self.train.get_exterior_light():
            self.extLightValue.setValue(100)
        else:
            self.extLightValue.setValue(0)
        self.extLightValue_tb.setChecked(self.train.get_exterior_light())

        if self.train.get_interior_light():
            self.intLightValue.setValue(100)
        else:
            self.intLightValue.setValue(0)
        self.intLightValue_tb.setChecked(self.train.get_interior_light())

        if self.train.get_left_door():
            self.leftDoorValue.setValue(100)
        else:
            self.leftDoorValue.setValue(0)
        self.leftDoorValue_tb.setChecked(self.train.get_left_door())

        if self.train.get_right_door():
            self.rightDoorValue.setValue(100)
        else:
            self.rightDoorValue.setValue(0)
        self.rightDoorValue_tb.setChecked(self.train.get_right_door())


# initialize the app
app = QApplication(sys.argv)
UIWindow = UITrain()
app.exec()

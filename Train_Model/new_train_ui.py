from PyQt6.QtGui import QIcon

import os
from PyQt6 import uic
from PyQt6.QtWidgets import (QMainWindow, QLabel, QPushButton, QGroupBox,
                             QCheckBox, QComboBox, QProgressBar, QLineEdit)
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import pyqtSlot

import random

from Train_Model.train_model_signals import train_model_signals


class UITrain(QMainWindow):
    # constants
    tons_per_kilogram = 0.00110231
    feet_per_meter = 3.28084

    def __init__(self):
        super(UITrain, self).__init__()

        # load the ui file
        current_dir = os.path.dirname(__file__)  # setting up to work in any dir
        ui_path = os.path.join(current_dir, 'Train_Model_UI.ui')
        try:
            uic.loadUi(ui_path, self)
        except Exception as e:
            print("Train Model UI: Error with loading UI file: ", e)

        # declare the train object
        self.train_dict = dict()
        self.signals = train_model_signals
        self.signals.pass_dict_to_ui.connect(self.dict_initialization)
        self.signals.ui_remove_train.connect(self.train_removed)
        self.signals.ui_add_train.connect(self.train_added)
        self.signals.index_update.connect(self.index_update)
        self.signals.total_update.connect(self.values_updated)
        self.signals.ui_initialization.emit()
        self.index: int
        if len(self.train_dict.keys()) == 0:
            self.index = 0
        else:
            self.index = min(self.train_dict.keys())

        # define widgets
        self.adLabel = self.findChild(QLabel, "adLabel")
        ad = random.randint(0, 2)
        if ad == 0:
            current_dir = os.path.dirname(__file__)  # setting up to work in any dir
            ad_path = os.path.join(current_dir, 'Aerotek.png')
        elif ad == 1:
            current_dir = os.path.dirname(__file__)  # setting up to work in any dir
            ad_path = os.path.join(current_dir, 'einsteins_ad.png')
        else:
            current_dir = os.path.dirname(__file__)  # setting up to work in any dir
            ad_path = os.path.join(current_dir, 'hat_ad.png')

        try:
            self.adLabel.setPixmap(QPixmap(ad_path))
        except Exception as e:
            print(f'Train Model UI: Error with ad {ad} file: ,', e)

        self.primeGroup = self.findChild(QGroupBox, "primeGroup")
        self.trainSelect = self.findChild(QComboBox, "trainSelect")
        self.trainSelect.clear()
        self.train_name_list = list()
        for i in self.train_dict.keys():
            self.train_name_list.append(f'Train {i}')
            self.trainSelect.addItem(f'Train {i}')
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
        self.totMassValue_tb = self.findChild(QLabel, "totMassValue_tb")
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
        current_dir = os.path.dirname(__file__)  # setting up to work in any dir
        icon_path = os.path.join(current_dir, 'red_triangle.png')
        try:
            self.emerButton.setIcon(QIcon(icon_path))
        except Exception as e:
            print("Train Model UI: Error with loading Icon file: ", e)

        self.phyGroup_tb.hide()
        self.trainGroup_tb.hide()
        self.transGroup_tb.hide()
        self.opGroup_tb.hide()
        self.tb = False
        self.ebp = False
        self.switching_trains = False
        self.vals_update = False

        self.trainSelect.currentIndexChanged.connect(self.combo_selection)

        self.emerButton.pressed.connect(self.set_pbrake)
        self.tbCheck.stateChanged.connect(self.tb_toggle)
        self.powerValue_tb.editingFinished.connect(self.power_change)
        self.accValue_tb.editingFinished.connect(self.acc_change)
        self.speedValue_tb.editingFinished.connect(self.speed_change)
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

    @pyqtSlot(dict)
    def values_updated(self, train_dict: dict):
        self.train_dict = train_dict
        self.vals_update = True
        self.populate_values()
        self.vals_update = False

    @pyqtSlot(dict, int)
    def index_update(self, train_dict: dict, index: int):
        self.train_dict = train_dict
        string = str(self.trainSelect.currentText())
        if int(string[6:]) == index:
            self.populate_values()

    @pyqtSlot(dict, int)
    def train_added(self, train_dict: dict, index: int):
        self.train_dict = train_dict
        self.train_name_list.append(f'Train {index}')
        self.trainSelect.addItem(f'Train {index}')

    @pyqtSlot(dict, int)
    def train_removed(self, train_dict: dict, index: int):
        self.train_dict = train_dict
        if f'Train {index}' in self.train_name_list:
            self.trainSelect.clear()
            self.train_name_list.remove(f'Train {index}')
            for name in self.train_name_list:
                self.trainSelect.addItem(name)
            if len(self.train_name_list) != 0:
                self.combo_selection()

    def combo_selection(self):
        if len(self.train_name_list) == 0:
            return
        string = str(self.trainSelect.currentText())
        if not ('Train' in string):
            return
        self.index = int(string[6:])
        self.switching_trains = True
        self.populate_values()
        self.switching_trains = False

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

    def set_pbrake(self):
        self.train_dict[self.index].brakes.passenger_ebrake = True
        self.ebp = True
        self.populate_values()
        self.ebp = False
        self.signals.ui_update.emit(self.train_dict)

    def power_change(self):
        if not self.switching_trains:
            self.train_dict[self.index].engine.set_power(float(self.powerValue_tb.text()))
            self.populate_values()
            self.signals.ui_update.emit(self.train_dict)

    def acc_change(self):
        if not self.switching_trains:
            self.train_dict[self.index].acceleration = float(self.accValue_tb.text()) / self.feet_per_meter
            self.populate_values()
            self.signals.ui_update.emit(self.train_dict)

    def speed_change(self):
        self.train_dict[self.index].set_velocity(float(self.speedValue_tb.text()) * 5280 / self.feet_per_meter / 3600)
        self.populate_values()
        self.signals.ui_update.emit(self.train_dict)

    def grade_change(self):
        if self.train_dict[self.index].position > self.train_dict[self.index].train_const.train_length() / 2:
            self.train_dict[self.index].new_block.grade = float(self.gradeValue_tb.text())
        else:
            self.train_dict[self.index].old_block.grade = float(self.gradeValue_tb.text())
        self.populate_values()
        self.signals.ui_update.emit(self.train_dict)

    def elev_change(self):
        if self.train_dict[self.index].position > self.train_dict[self.index].train_const.train_length() / 2:
            self.train_dict[self.index].new_block.elevation = float(self.elevValue_tb.text()) / self.feet_per_meter
        else:
            self.train_dict[self.index].old_block.elevation = float(self.elevValue_tb.text()) / self.feet_per_meter
        self.populate_values()
        self.signals.ui_update.emit(self.train_dict)

    def pbrake_change(self):
        if not self.switching_trains:
            if not self.ebp:
                self.train_dict[self.index].brakes.toggle_passenger_ebrake()
                self.populate_values()
        self.ebp = False
        self.signals.ui_update.emit(self.train_dict)

    def sbrake_change(self):
        if not (self.switching_trains or self.vals_update):
            self.train_dict[self.index].brakes.toggle_service_brake()
            self.populate_values()
            self.signals.ui_update.emit(self.train_dict)

    def dbrake_change(self):
        if not (self.switching_trains or self.vals_update):
            self.train_dict[self.index].brakes.toggle_driver_ebrake()
            self.populate_values()
            self.signals.ui_update.emit(self.train_dict)

    def cars_change(self):
        self.train_dict[self.index].train_const.set_cars(int(self.carsValue_tb.text()))
        self.populate_values()
        self.signals.ui_update.emit(self.train_dict)

    def crew_change(self):
        self.train_dict[self.index].crew.set_people(int(self.crewValue_tb.text()))
        self.populate_values()
        self.signals.ui_update.emit(self.train_dict)

    def pass_change(self):
        self.train_dict[self.index].passengers.set_people(int(self.passValue_tb.text()),
                                                          self.train_dict[self.index].train_const.max_passengers())
        self.populate_values()
        self.signals.ui_update.emit(self.train_dict)

    def engine_change(self):
        if not self.switching_trains:
            self.train_dict[self.index].failure.toggle_engine()
            self.populate_values()
            self.signals.ui_update.emit(self.train_dict)

    def signal_change(self):
        if not self.switching_trains:
            self.train_dict[self.index].failure.toggle_signal_pickup()
            self.populate_values()
            self.signals.ui_update.emit(self.train_dict)

    def brake_change(self):
        if not self.switching_trains:
            self.train_dict[self.index].failure.toggle_brakes()
            self.populate_values()
            self.signals.ui_update.emit(self.train_dict)

    def rec_speed_changed(self):
        self.train_dict[self.index].signals.set_commanded_speed(float(self.recSpeedValue_tb.text()),
                                                                self.train_dict[self.index].failure.
                                                                signal_pickup_failure)
        self.populate_values()
        self.signals.ui_update.emit(self.train_dict)

    def auth_changed(self):
        self.train_dict[self.index].signals.set_authority(int(self.authValue_tb.text(), 16),
                                                          self.train_dict[self.index].failure.signal_pickup_failure)
        self.populate_values()
        self.signals.ui_update.emit(self.train_dict)

    def beacon_changed(self):
        self.train_dict[self.index].signals.beacon = self.beaconValue_tb.text()
        self.populate_values()
        self.signals.ui_update.emit(self.train_dict)

    def temp_change(self):
        self.train_dict[self.index].heater.update_target(float(self.tempValue_tb.text()))
        self.populate_values()
        self.signals.ui_update.emit(self.train_dict)

    def ext_light_change(self):
        if not (self.switching_trains or self.vals_update):
            self.train_dict[self.index].interior_functions.toggle_exterior_lights()
            self.populate_values()
            self.signals.ui_update.emit(self.train_dict)

    def int_light_change(self):
        if not (self.switching_trains or self.vals_update):
            self.train_dict[self.index].interior_functions.toggle_interior_lights()
            self.populate_values()
            self.signals.ui_update.emit(self.train_dict)

    def left_door_change(self):
        if not (self.switching_trains or self.vals_update):
            self.train_dict[self.index].interior_functions.toggle_left_doors()
            self.populate_values()
            self.signals.ui_update.emit(self.train_dict)

    def right_door_change(self):
        if not (self.switching_trains or self.vals_update):
            self.train_dict[self.index].interior_functions.toggle_right_doors()
            self.populate_values()
            self.signals.ui_update.emit(self.train_dict)

    @pyqtSlot(dict)
    def dict_initialization(self, train_dict: dict):
        self.train_dict = train_dict

    def populate_values(self):
        if self.index not in self.train_dict.keys():
            return

        self.powerValue.setText(f'{self.train_dict[self.index].engine.power: .2f} W')
        self.powerValue_tb.setText(f'{self.train_dict[self.index].engine.power: .2f}')

        self.accValue.setText(
            f"{self.train_dict[self.index].acceleration * self.feet_per_meter: .2f} ft/s<sup>2")
        self.accValue_tb.setText(f"{self.train_dict[self.index].acceleration * self.feet_per_meter: .2f}")

        self.speedValue.setText(f'{self.train_dict[self.index].velocity * self.feet_per_meter * 3600 / 5280: .2f} mph')
        self.speedValue_tb.setText(f'{self.train_dict[self.index].velocity * self.feet_per_meter * 3600 / 5280: .2f}')

        self.totMassValue.setText(f'{self.train_dict[self.index].get_total_mass() * self.tons_per_kilogram: .2f} Tons')
        self.totMassValue_tb.setText(
            f'{self.train_dict[self.index].get_total_mass() * self.tons_per_kilogram: .2f} Tons')

        if self.train_dict[self.index].position > self.train_dict[self.index].train_const.train_length() / 2:
            self.gradeValue.setText(f'{self.train_dict[self.index].new_block.grade: .2f} %')
            self.gradeValue_tb.setText(f'{self.train_dict[self.index].new_block.grade: .2f}')
        else:
            self.gradeValue.setText(f'{self.train_dict[self.index].old_block.grade: .2f} %')
            self.gradeValue_tb.setText(f'{self.train_dict[self.index].old_block.grade: .2f}')

        if self.train_dict[self.index].position > self.train_dict[self.index].train_const.train_length() / 2:
            self.elevValue.setText(f'{self.train_dict[self.index].new_block.elevation * self.feet_per_meter: .2f} ft')
            self.elevValue_tb.setText(f'{self.train_dict[self.index].new_block.elevation * self.feet_per_meter: .2f}')
        else:
            self.elevValue.setText(f'{self.train_dict[self.index].old_block.elevation * self.feet_per_meter: .2f} ft')
            self.elevValue_tb.setText(f'{self.train_dict[self.index].old_block.elevation * self.feet_per_meter: .2f}')

        if self.train_dict[self.index].brakes.passenger_ebrake:
            self.pBrakeValue.setValue(100)
        else:
            self.pBrakeValue.setValue(0)
        self.pBrakeValue_tb.setChecked(self.train_dict[self.index].brakes.passenger_ebrake)

        if self.train_dict[self.index].brakes.service_brake:
            self.sBrakeValue.setValue(100)
        else:
            self.sBrakeValue.setValue(0)
        self.sBrakeValue_tb.setChecked(self.train_dict[self.index].brakes.service_brake)

        if self.train_dict[self.index].brakes.driver_ebrake:
            self.dBrakeValue.setValue(100)
        else:
            self.dBrakeValue.setValue(0)
        self.dBrakeValue_tb.setChecked(self.train_dict[self.index].brakes.driver_ebrake)

        self.lengthValue.setText(
            f'{self.train_dict[self.index].train_const.train_length() * self.feet_per_meter: .2f} ft')
        self.lengthValue_tb.setText(
            f'{self.train_dict[self.index].train_const.train_length() * self.feet_per_meter: .2f} ft')

        self.heightValue.setText(f'{self.train_dict[self.index].train_const.height * self.feet_per_meter: .2f} ft')
        self.heightValue_tb.setText(f'{self.train_dict[self.index].train_const.height * self.feet_per_meter: .2f} ft')

        self.widthValue.setText(f'{self.train_dict[self.index].train_const.width * self.feet_per_meter: .2f} ft')
        self.widthValue_tb.setText(f'{self.train_dict[self.index].train_const.width * self.feet_per_meter: .2f} ft')

        self.carsValue.setText(f'{self.train_dict[self.index].train_const.car_number}')
        self.carsValue_tb.setText(f'{self.train_dict[self.index].train_const.car_number}')

        self.trainMassValue.setText(
            f'{self.train_dict[self.index].train_const.train_mass() * self.tons_per_kilogram: .2f} Tons')
        self.trainMassValue_tb.setText(
            f'{self.train_dict[self.index].train_const.train_mass() * self.tons_per_kilogram: .2f} Tons')

        self.crewValue.setText(f'{self.train_dict[self.index].crew.people_number}')
        self.crewValue_tb.setText(f'{self.train_dict[self.index].crew.people_number}')

        self.passValue.setText(f'{self.train_dict[self.index].passengers.people_number}')
        self.passValue_tb.setText(f'{self.train_dict[self.index].passengers.people_number}')

        self.eFailCheck.setChecked(self.train_dict[self.index].failure.engine_failure)
        self.sFailCheck.setChecked(self.train_dict[self.index].failure.signal_pickup_failure)
        self.bFailCheck.setChecked(self.train_dict[self.index].failure.brake_failure)

        self.recSpeedValue.setText(f'{self.train_dict[self.index].signals.commanded_speed: .2f}')
        self.recSpeedValue_tb.setText(f'{self.train_dict[self.index].signals.commanded_speed: .2f}')

        self.authValue.setText(f'{self.train_dict[self.index].signals.authority}')
        self.authValue_tb.setText(f'{self.train_dict[self.index].signals.authority}')
        self.beaconValue.setText(self.train_dict[self.index].signals.beacon)
        self.beaconValue_tb.setText(self.train_dict[self.index].signals.beacon)

        self.tempValue.setText(f'{self.train_dict[self.index].heater.current_temp: .2f} °F')
        self.tempValue_tb.setText(f'{self.train_dict[self.index].heater.current_temp: .2f}')

        if self.train_dict[self.index].interior_functions.exterior_lights:
            self.extLightValue.setValue(100)
        else:
            self.extLightValue.setValue(0)
        self.extLightValue_tb.setChecked(self.train_dict[self.index].interior_functions.exterior_lights)

        if self.train_dict[self.index].interior_functions.interior_lights:
            self.intLightValue.setValue(100)
        else:
            self.intLightValue.setValue(0)
        self.intLightValue_tb.setChecked(self.train_dict[self.index].interior_functions.interior_lights)

        if self.train_dict[self.index].interior_functions.left_doors:
            self.leftDoorValue.setValue(100)
        else:
            self.leftDoorValue.setValue(0)
        self.leftDoorValue_tb.setChecked(self.train_dict[self.index].interior_functions.left_doors)

        if self.train_dict[self.index].interior_functions.right_doors:
            self.rightDoorValue.setValue(100)
        else:
            self.rightDoorValue.setValue(0)
        self.rightDoorValue_tb.setChecked(self.train_dict[self.index].interior_functions.right_doors)


# initialize the app
# app = QApplication(sys.argv)
# UIWindow = UITrain()
# UIWindow.show()
# app.exec()


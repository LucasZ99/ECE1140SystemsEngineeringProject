import sys

from PyQt6.QtCore import QObject, pyqtSignal
from PyQt6.QtWidgets import QApplication

from Train_Model import TrainBusinessLogic, TrainModel, UITrain
import trainControllerTot_Container


class TrainModelContainer(QObject):

    passenger_return = dict()
    ui_list = list()
    business_logic = TrainBusinessLogic()
    num_cars = 1
    new_train_added = pyqtSignal(int)
    train_enters_new_block = pyqtSignal(int)

    def __init__(self, bus: TrainBusinessLogic(), controller: trainControllerTot_Container):
        super().__init__()
        self.business_logic = bus
        self.train_list = self.business_logic.train_list
        self.controller = controller

    def track_model_inputs(self, input_list, index):
        # the list provided should have entries in this order: [commanded speed, vital authority, beacon, underground]
        if len(self.train_list) == 0:
            return False
        elif not (index in self.train_list.keys()):
            return False
        else:
            self.train_list[index].signals.set_commanded_speed(input_list[0],
                                                               self.train_list[index].failure.signal_pickup_failure)
            self.train_list[index].signals.set_authority(input_list[1],
                                                         self.train_list[index].failure.signal_pickup_failure)
            self.train_list[index].signals.beacon = input_list[2]
            self.train_list[index].underground = input_list[3]
            # [actual speed, authority, received speed, pbrake, track circuit, underground, beacon]
            self.controller.updatevalues([self.train_list[index].velocity, input_list[1], input_list[0],
                                          self.train_list[index].brakes.passenger_ebrake,
                                          self.train_list[index].track_circuit, input_list[3], input_list[2]])
            self.business_logic.values_updated.emit()
            return True

    def train_controller_inputs(self, input_list, index):
        # the list provided should have the entries in this order: [commanded speed, power, service brake,
        # emergency brake, left/right doors, announce station, cabin lights, headlights]
        if len(self.train_list) == 0:
            return False
        if not (index in self.train_list.keys()):
            return False
        else:
            # train controller inputs: [commanded speed, power, service brake, emergency brake, left/right doors,
            # announce station, cabin lights, headlights]
            self.train_list[index].engine.set_power(input_list[1])
            self.train_list[index].brakes.service_brake = input_list[2]
            self.train_list[index].brakes.driver_ebrake = input_list[3]
            self.train_list[index].interior_functions.left_doors = (int(input_list[4] % 2) == 1)
            self.train_list[index].interior_functions.right_doors = (int(input_list[4] / 2) == 1)
            self.train_list[index].interior_functions.announcement = input_list[5]
            self.train_list[index].interior_functions.interior_lights = input_list[6]
            self.train_list[index].interior_functions.exterior_lights = input_list[7]
            self.business_logic.values_updated.emit()
            return True

    def track_update_block(self, block_vals, index):
        if not (index in self.train_list.keys()):
            return False
        # block_vals should be a list as such: [grade, elevation, block length]
        self.train_list[index].update_blocks(block_vals)
        self.business_logic.block_updated.emit(index)
        return True

    def track_update_passengers(self, num, index):
        if not (index in self.train_list.keys()):
            return False
        self.passenger_return[index] = self.train_list[index].passengers.update_at_station(num, self.train_list[index].train_const.max_passengers())
        self.business_logic.passengers_updated(index)
        return True

    def controller_update_temp(self, num, index):
        if not (index in self.train_list.keys()):
            return False
        self.train_list[index].heater.update_target(num)
        self.business_logic.temp_updated(index)
        return True

    def physics_calculation(self, time):
        for i in self.train_list:
            self.train_list[i].physics_calculation(time)
            if self.train_list[i].position > self.train_list[i].new_block.block_length:
                self.train_list[i].track_circuit = not self.train_list[i].track_circuit
                self.train_enters_new_block.emit(i)
            self.controller.updatevalues([self.train_list[i].velocity, self.train_list[i].signals.authority,
                                          self.train_list[i].signals.commanded_speed,
                                          self.train_list[i].brakes.passenger_ebrake,
                                          self.train_list[i].track_circuit, self.train_list[i].underground,
                                          self.train_list[i].signals.beacon])
        self.business_logic.values_updated.emit()

    def add_train(self):
        if len(self.train_list) == 0:
            self.train_list[1] = TrainModel(1, self.num_cars)
            index = 1
        else:
            index = max(self.train_list.keys()) + 1
            self.train_list[index] = TrainModel(index, self.num_cars)

        self.business_logic.train_added.emit(index)
        self.new_train_added.emit(index)
        return index

    def remove_train(self, index):
        if not (index in self.train_list.keys()):
            return False
        else:
            self.train_list.pop(index)
            self.business_logic.train_removed.emit(index)
            return True

    def show_ui(self):
        app = QApplication.instance()

        if app is None:
            app = QApplication([])

        self.ui = UITrain(self.business_logic)
        self.ui.show()

        app.exec()

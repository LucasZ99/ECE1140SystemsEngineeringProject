from PyQt6.QtCore import pyqtSignal, QObject, pyqtSlot

import SystemTime
from Train_Model.new_train_model import TrainModel
from trainControllerTot_Container import TrainController_Tot_Container
from Train_Model.train_model_signals import train_model_signals


class TrainBusinessLogic(QObject):

    # declare signals
    num_cars = 1
    train_dict = dict()
    delta_x_return = dict()
    passenger_return = dict()
    
    def __init__(self):
        super().__init__()
        self.time = SystemTime.time()
        self.controller = TrainController_Tot_Container()
        self.signals = train_model_signals
        self.signals.clear_return_dicts.connect(self.clear_dicts)
        self.signals.send_back_track_returns.connect(self.return_to_container)
        self.signals.physics_calculation.connect(self.physics_calculation)
        self.signals.train_update_controller.connect(self.train_update_controller)
        self.signals.track_update_passenger.connect(self.track_update_passengers)
        self.signals.track_update_block.connect(self.track_update_block)
        self.signals.track_model_inputs.connect(self.track_model_inputs)
        self.signals.business_add_train.connect(self.add_train)
        self.signals.clear_return_dicts.connect(self.clear_dicts)
        self.signals.send_back_track_returns.connect(self.return_to_container)
        self.signals.business_remove_train.connect(self.remove_train)
        self.signals.ui_initialization.connect(self.pass_dict_to_ui)
        self.signals.ui_update.connect(self.ui_update)
        self.signals.controller_update_temp.connect(self.controller_update_temp)
        self.signals.train_controller_inputs.connect(self.train_controller_inputs)

    @pyqtSlot(tuple, int)
    def track_model_inputs(self, input_list, index):
        if len(self.train_dict) == 0:
            return
        elif not (index in self.train_dict.keys()):
            return
        else:
            self.train_dict[index].signals.set_commanded_speed(input_list[0],
                                                               self.train_dict[index].failure.signal_pickup_failure)
            self.train_dict[index].signals.set_authority(input_list[1],
                                                         self.train_dict[index].failure.signal_pickup_failure)

            print("train's track model inputs updated")
            self.signals.index_update.emit(self.train_dict, index)

    @pyqtSlot(tuple, int)
    def train_controller_inputs(self, input_list, index):
        # [commanded speed, power, service brake, emergency brake, left/right doors, announce station, cabin lights,
        # headlights]
        if len(self.train_dict) == 0:
            return
        if not (index in self.train_dict.keys()):
            return
        else:
            self.train_dict[index].engine.set_power(input_list[1])
            self.train_dict[index].brakes.service_brake = input_list[2]
            self.train_dict[index].brakes.driver_ebrake = input_list[3]
            self.train_dict[index].brakes.passenger_ebrake_ebrake = input_list[3]
            self.train_dict[index].interior_functions.left_doors = (int(input_list[4] % 2) == 1)
            self.train_dict[index].interior_functions.right_doors = (int(input_list[4] / 2) == 1)
            self.train_dict[index].interior_functions.announcement = input_list[5]
            self.train_dict[index].interior_functions.interior_lights = input_list[6]
            self.train_dict[index].interior_functions.exterior_lights = input_list[7]
            self.signals.index_update.emit(self.train_dict, index)

    @pyqtSlot(tuple, int)
    def track_update_block(self, block_vals, index):
        if len(self.train_dict) == 0:
            return
        if not (index in self.train_dict.keys()):
            return
        self.train_dict[index].update_blocks(block_vals[:3])
        self.train_dict[index].signals.beacon = block_vals[3]
        self.signals.index_update.emit(self.train_dict, index)

    @pyqtSlot(int, int)
    def track_update_passengers(self, num, index):
        if len(self.train_dict) == 0:
            return
        if not (index in self.train_dict.keys()):
            return
        self.passenger_return[index] = self.train_dict[index].passengers.update_at_station(num, self.train_dict[index].
                                                                                           train_const.max_passengers())
        self.signals.index_update.emit(self.train_dict, index)

    @pyqtSlot(float, int)
    def controller_update_temp(self, num, index):
        if len(self.train_dict) == 0:
            return
        if not (index in self.train_dict.keys()):
            return
        self.train_dict[index].heater.update_target(num)
        self.signals.index_update.emit(self.train_dict, index)

    @pyqtSlot()
    def physics_calculation(self):
        interval = SystemTime.time() - self.time
        self.time = SystemTime.time()
        for i in self.train_dict:
            self.delta_x_return[i] = self.train_dict[i].physics_calculation(interval)
        self.signals.total_update.emit(self.train_dict)

    @pyqtSlot()
    def add_train(self):
        self.time = SystemTime.time()
        if len(self.train_dict) == 0:
            self.train_dict[1] = TrainModel(self.controller, 1, self.num_cars)
            index = 1
        else:
            index = max(self.train_dict.keys()) + 1
            self.train_dict[index] = TrainModel(self.controller, index, self.num_cars)
        self.signals.ui_add_train.emit(self.train_dict, index)

    @pyqtSlot(int)
    def remove_train(self, index):
        if len(self.train_dict) == 0:
            return
        if not (index in self.train_dict.keys()):
            return
        else:
            self.train_dict.pop(index)
            self.signals.ui_remove_train.emit(self.train_dict, index)

    @pyqtSlot()
    def train_update_controller(self):
        for i in self.train_dict.keys():
            self.train_dict[i].update_controller()
        self.signals.total_update.emit(self.train_dict)

    @pyqtSlot()
    def clear_dicts(self):
        self.delta_x_return.clear()
        self.passenger_return.clear()

    @pyqtSlot()
    def return_to_container(self):
        self.signals.business_update(self.delta_x_return, self.passenger_return)

    @pyqtSlot()
    def pass_dict_to_ui(self):
        self.signals.pass_dict_to_ui.emit(self.train_dict)

    @pyqtSlot(dict)
    def ui_update(self, train_dict: dict):
        self.train_dict = train_dict

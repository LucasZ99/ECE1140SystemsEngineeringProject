from PyQt6.QtCore import pyqtSignal, QObject, pyqtSlot
from SystemTime import SystemTimeContainer
from Train_Model.new_train_model import TrainModel
from trainControllerTot_Container import TrainController_Tot_Container


class TrainBusinessLogic(QObject):

    # declare signals
    num_cars = 1
    train_dict: dict
    delta_x_return: dict
    passenger_return: dict
    values_updated = pyqtSignal()
    block_updated = pyqtSignal(int)
    passengers_updated = pyqtSignal(int)
    temp_updated = pyqtSignal(int)
    train_added = pyqtSignal(int)
    train_removed = pyqtSignal(int)
    
    def __init__(self, time: SystemTimeContainer):
        super().__init__()
        self.time_keeper = time
        self.time = self.time_keeper.system_time.time()

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

            self.physics_calculation()
            self.values_updated.emit()
            print("train's track model inputs updated")

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
            self.values_updated.emit()

    def track_update_block(self, block_vals, index):
        if len(self.train_dict) == 0:
            return
        if not (index in self.train_dict.keys()):
            return
        self.train_dict[index].update_blocks(block_vals[:4])
        self.train_dict[index].signals.beacon = block_vals[4]
        self.block_updated.emit(index)

    def track_update_passengers(self, num, index):
        if len(self.train_dict) == 0:
            return
        if not (index in self.train_dict.keys()):
            return
        self.passenger_return[index] = self.train_dict[index].passengers.update_at_station(num, self.train_dict[index].
                                                                                           train_const.max_passengers())
        self.passengers_updated.emit(index)

    def controller_update_temp(self, num, index):
        if len(self.train_dict) == 0:
            return
        if not (index in self.train_dict.keys()):
            return
        self.train_dict[index].heater.update_target(num)
        self.temp_updated.emit(index)

    def physics_calculation(self):
        interval = self.time_keeper.system_time.time() - self.time
        self.time = self.time_keeper.system_time.time()
        for i in self.train_dict:
            self.delta_x_return[i] = self.train_dict[i].physics_calculation(interval)
        self.values_updated.emit()

    def add_train(self, controller_container: TrainController_Tot_Container):
        self.time = self.time_keeper.system_time.time()
        if len(self.train_dict) == 0:
            self.train_dict[1] = TrainModel(controller_container, 1, self.num_cars)
            index = 1
        else:
            index = max(self.train_dict.keys()) + 1
            self.train_dict[index] = TrainModel(controller_container, index, self.num_cars)
        self.train_added.emit(index)

    def remove_train(self, index):
        if len(self.train_dict) == 0:
            return
        if not (index in self.train_dict.keys()):
            return
        else:
            self.train_dict.pop(index)
            self.train_removed.emit(index)

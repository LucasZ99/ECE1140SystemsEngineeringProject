import sys

from PyQt6.QtCore import QObject, pyqtSignal
from PyQt6.QtWidgets import QApplication

from Train_Model import TrainBusinessLogic, TrainModel, UITrain
from trainControllerTot_Container import TrainController_Tot_Container
from SystemTime import SystemTimeContainer


class TrainModelContainer(QObject):
    passenger_return = dict()
    ui_list = list()
    business_logic = TrainBusinessLogic()
    num_cars = 1
    new_train_added = pyqtSignal(int)
    train_enters_new_block = pyqtSignal(int)

    def __init__(self, bus: TrainBusinessLogic(), controller: TrainController_Tot_Container, time: SystemTimeContainer):
        super().__init__()
        self.business_logic = bus
        self.train_list = self.business_logic.train_list
        self.controller = controller
        self.controller.new_train_values_signal.connect(self.train_controller_inputs)
        self, controller.new_train_temp_signal.connect(self.controller_update_temp)
        self.time_keeper = time
        self.time = self.time_keeper.system_time.time()
        self.business_logic.ui_updates.connect(self.ui_updates)

    def track_model_inputs(self, input_list, index):
        print("train's track model inputs hit")
        
        print(f"track_model_inputs: {index}, {input_list}")
        
        # the list provided should have entries in this order: [commanded speed, vital authority]
        if len(self.train_list) == 0:
            return
        elif not (index in self.train_list.keys()):
            return
        else:
            self.train_list[index].signals.set_commanded_speed(input_list[0],
                                                               self.train_list[index].failure.signal_pickup_failure)
            self.train_list[index].signals.set_authority(input_list[1],
                                                         self.train_list[index].failure.signal_pickup_failure)

            self.controller.getvaluesfromtrain(
                [self.train_list[index].velocity, 
                 self.train_list[index].signals.commanded_speed, 
                 self.train_list[index].signals.authority,
                 self.train_list[index].brakes.passenger_ebrake,
                 self.train_list[index].track_circuit, self.train_list[index].underground,
                 self.train_list[index].signals.beacon])
            self.physics_calculation()
            self.business_logic.train_list = self.train_list
            print("train's track model inputs updated")
            self.business_logic.values_updated.emit()

    def train_controller_inputs(self, input_list, index):
        print("Train model: train_controller_inputs called")
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
            self.business_logic.train_list = self.train_list
            self.business_logic.values_updated.emit()

    def track_update_block(self, block_vals, index):
        
        print(f"track_update_block: {index}, {block_vals}")
        
        if not (index in self.train_list.keys()):
            return
        # block_vals should be a list as such: [grade, elevation, block length, underground, beacon]
        self.train_list[index].update_blocks(block_vals[:4])
        self.train_list[index].signals.beacon = block_vals[4]
        self.controller.getvaluesfromtrain([self.train_list[index].velocity, 
                                            self.train_list[index].signals.commanded_speed, 
                                            self.train_list[index].signals.authority,
                                            self.train_list[index].brakes.passenger_ebrake,
                                            self.train_list[index].track_circuit, self.train_list[index].underground,
                                            self.train_list[index].signals.beacon])
        self.business_logic.block_updated.emit(index)
        self.business_logic.train_list = self.train_list

    def track_update_passengers(self, num, index):
        if not (index in self.train_list.keys()):
            return
        self.passenger_return[index] = self.train_list[index].passengers.update_at_station(num, self.train_list[
            index].train_const.max_passengers())
        self.business_logic.passengers_updated.emit(index)
        self.business_logic.train_list = self.train_list

    def controller_update_temp(self, num, index):
        if not (index in self.train_list.keys()):
            return
        self.train_list[index].heater.update_target(num)
        self.business_logic.temp_updated.emit(index)
        self.business_logic.train_list = self.train_list

    def physics_calculation(self):
        interval = self.time_keeper.system_time.time() - self.time
        self.time = self.time_keeper.system_time.time()
        for i in self.train_list:
            self.train_list[i].physics_calculation(interval)
            if self.train_list[i].position > self.train_list[i].new_block.block_length:
                self.train_list[i].track_circuit = not self.train_list[i].track_circuit
                self.train_enters_new_block.emit(i)
            self.controller.getvaluesfromtrain([self.train_list[i].velocity, self.train_list[i].signals.commanded_speed, 
                                                self.train_list[i].signals.authority,
                                                self.train_list[i].brakes.passenger_ebrake,
                                                self.train_list[i].track_circuit, self.train_list[i].underground,
                                                self.train_list[i].signals.beacon])
        self.business_logic.values_updated.emit()
        self.business_logic.train_list = self.train_list

    def add_train(self):
        print("train endpoint hit")
        if len(self.train_list) == 0:
            self.train_list[1] = TrainModel(1, self.num_cars)
            index = 1
        else:
            index = max(self.train_list.keys()) + 1
            self.train_list[index] = TrainModel(index, self.num_cars)

        self.business_logic.train_list = self.train_list
        self.business_logic.train_added.emit(index)
        self.new_train_added.emit(index)
        print("train added in train container")

    def remove_train(self, index):

        if not (index in self.train_list.keys()):
            return
        else:
            self.train_list.pop(index)
            self.business_logic.train_removed.emit(index)
            self.business_logic.train_list = self.train_list

    def ui_updates(self):
        for i in self.train_list.keys():
            self.controller.getvaluesfromtrain([self.train_list[i].velocity, self.train_list[i].signals.commanded_speed,
                                                self.train_list[i].signals.authority,
                                                self.train_list[i].brakes.passenger_ebrake,
                                                self.train_list[i].track_circuit, self.train_list[i].underground,
                                                self.train_list[i].signals.beacon])

    def show_ui(self):
        app = QApplication.instance()

        if app is None:
            app = QApplication([])

        self.ui = UITrain(self.business_logic)
        self.ui.show()

        app.exec()

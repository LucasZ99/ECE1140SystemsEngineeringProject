import sys
from Train_Model import TrainBusinessLogic, TrainModel


class TrainModelContainer:

    track_inputs = dict()
    controller_inputs = dict()
    passenger_return = dict()
    ui_list = list()
    business_logic = TrainBusinessLogic()
    num_cars = 1

    def __init__(self, bus=TrainBusinessLogic()):
        self.business_logic = bus
        self.train_list = self.business_logic.train_list

    def track_model_inputs(self, input_list, index):
        # the list provided should have entries in this order: [commanded speed, vital authority, beacon, underground]
        if len(self.track_inputs) == 0:
            return False
        elif not (index in self.track_inputs.keys()):
            return False
        else:
            self.track_inputs[index] = input_list
            return True

    def train_controller_inputs(self, input_list, index):
        # the list provided should have the entries in this order: [commanded speed, power, service brake,
        # emergency brake, left/right doors, announce station, cabin lights, headlights]
        if len(self.controller_inputs) == 0:
            return False
        if not (index in self.controller_inputs.keys()):
            return False
        else:
            self.controller_inputs[index] = input_list
            return True

    def update_values(self):
        for i in self.train_list.keys():
            # track input list : [commanded speed, vital authority, beacon,  underground]
            self.train_list[i].signals.set_commanded_speed(self.track_inputs[i][0], self.train_list[i].failure.signal_pickup_failure)
            self.train_list[i].signals.set_authority(self.track_inputs[i][1], self.train_list[i].failure.signal_pickup_failure)
            self.train_list[i].signals.beacon = self.track_inputs[i][2]
            # train controller inputs: [commanded speed, power, service brake, emergency brake, left/right doors,
            # announce station, cabin lights, headlights]
            self.train_list[i].engine.set_power(self.controller_inputs[i][1])
            self.train_list[i].brakes.service_brake = self.controller_inputs[i][2]
            self.train_list[i].brakes.driver_ebrake = self.controller_inputs[i][3]
            self.train_list[i].interior_functions.left_doors = (int(self.controller_inputs[i][4] % 2) == 1)
            self.train_list[i].interior_functions.right_doors = (int(self.controller_inputs[i][4] / 2) == 1)
            self.train_list[i].interior_functions.announcement = self.controller_inputs[i][5]
            self.train_list[i].interior_functions.interior_lights = self.controller_inputs[i][6]
            self.train_list[i].interior_functions.exterior_lights = self.controller_inputs[i][7]
        self.business_logic.values_updated.emit()

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
        self.business_logic.values_updated.emit()

    def add_train(self):
        if len(self.train_list) == 0:
            self.train_list[1] = TrainModel(1, self.num_cars)
            self.track_inputs[1] = [0.0, 0, "", False]
            self.controller_inputs[1] = [0.0, 0.0, False, False, False, "", True, False]

            index = 1
        else:
            index = max(self.train_list.keys()) + 1
            self.train_list[index] = TrainModel(index, self.num_cars)
            self.track_inputs[index] = [0.0, 0, "", False]
            self.controller_inputs[index] = [0.0, 0.0, False, False, False, "", True, False,]

        self.business_logic.train_added.emit(index)
        return index

    def remove_train(self, index):
        if not (index in self.train_list.keys()):
            return False
        else:
            self.train_list.pop(index)
            self.track_inputs.pop(index)
            self.controller_inputs.pop(index)
            self.business_logic.train_removed.emit(index)
            return True



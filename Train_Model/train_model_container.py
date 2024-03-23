import sys
import new_train_model
import new_train_ui
from PyQt5.QtWidgets import (QApplication)


class TrainModelContainer:

    train_list = dict()
    track_inputs = dict()
    controller_inputs = dict()
    passenger_return = dict()
    ui_list = list()

    def __init__(self):
        # app = QApplication(sys.argv)
        # self.ui_list.append(new_train_ui.UITrain())
        # app.exec()

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

    def track_update_block(self, block_vals, index):
        if not (index in self.train_list.keys()):
            return False
        # block_vals should be a list as such: [grade, elevation, block length]
        self.train_list[index].update_blocks(block_vals)
        return True

    def track_update_passengers(self, num, index):
        if not (index in self.train_list.keys()):
            return False
        self.passenger_return[index] = self.train_list[index].passengers.update_at_station(num, self.train_list[index].train_const.max_passengers())
        return True

    def controller_update_temp(self, num, index):
        if not (index in self.train_list.keys()):
            return False
        self.train_list[index].heater.update_target(num)
        return True

    def physics_calculation(self, time):
        for i in self.train_list:
            self.train_list[i].physics_calculation(time)

    def add_train(self):
        if len(self.train_list) == 0:
            self.train_list[1] = new_train_model.TrainModel()
            self.track_inputs[1] = [0.0, 0, "", False]
            self.controller_inputs[1] = [0.0, 0.0, False, False, False, "", True, False]
            index = 1
        else:
            index = max(self.train_list.keys()) + 1
            self.train_list[index] = new_train_model.TrainModel()
            self.track_inputs[index] = [0.0, 0, "", False]
            self.controller_inputs[index] = [0.0, 0.0, False, False, False, "", True, False,]

        return index

    def remove_train(self, index):
        if not (index in self.train_list.keys()):
            return False
        else:
            self.train_list.pop(index)
            self.track_inputs.pop(index)
            self.controller_inputs.pop(index)
            return True


container = TrainModelContainer()
# container is empty
print(container.track_model_inputs([0, 0, "", False], 23))
print(container.train_controller_inputs([0, 0], 23))
print(container.track_update_block([0, 0, 0], 23))
print(container.track_update_passengers(23, 23))
print(container.controller_update_temp(23, 23))
print(container.remove_train(23))

container.add_train()
# container is not empty
# [commanded speed, vital authority, beacon, underground]
print(container.track_model_inputs([1, 1, "a", True], 1))
print(f'[{container.train_list[1].signals.commanded_speed}, {container.train_list[1].signals.authority}, '
      f'{container.train_list[1].signals.beacon}]')
container.update_values()
print(f'[{container.train_list[1].signals.commanded_speed}, {container.train_list[1].signals.authority}, '
      f'{container.train_list[1].signals.beacon}]')
print(container.track_model_inputs([0, 0, "", True], 2))

# [commanded speed, power, service brake, emergency brake, left/right doors, announce station, cabin lights, headlights]
print(container.train_controller_inputs([1, 1, True, True, 1, "a", False, True], 1))
container.update_values()
print(f'[{container.train_list[1].engine.power}, {container.train_list[1].brakes.service_brake}, '
      f'{container.train_list[1].brakes.driver_ebrake}, {container.train_list[1].interior_functions.left_doors}, '
      f'{container.train_list[1].interior_functions.right_doors}, '
      f'{container.train_list[1].interior_functions.announcement}, '
      f'{container.train_list[1].interior_functions.interior_lights}, '
      f'{container.train_list[1].interior_functions.exterior_lights}]')
print(container.train_controller_inputs([0, 0, False, False, 0, "", True, False], 2))

print(container.track_update_block([1, 1, 1], 1))
print(f'[{container.train_list[1].new_block.grade}, {container.train_list[1].new_block.elevation}, '
      f'{container.train_list[1].new_block.block_length}]')
print(container.track_update_block([0, 0, 0], 2))

print(container.track_update_passengers(48, 1))
print(container.track_update_passengers(48, 1))
print(container.train_list[1].passengers.people_number)
print(container.track_update_passengers(47, 2))

print(container.controller_update_temp(70, 1))
print(container.train_list[1].heater.target_temp)
print(container.controller_update_temp(70, 2))

container.physics_calculation(1)

print(container.remove_train(2))
print(container.remove_train(1))

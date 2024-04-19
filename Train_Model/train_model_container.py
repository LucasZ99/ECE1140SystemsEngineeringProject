import sys

from PyQt6.QtCore import QObject, pyqtSignal, pyqtSlot
from PyQt6.QtWidgets import QApplication

from Train_Model import TrainBusinessLogic, UITrain
from trainControllerTot_Container import TrainController_Tot_Container
from SystemTime import SystemTimeContainer


class TrainModelContainer(QObject):
    update_track_model_from_train_model = pyqtSignal(object, object)

    def __init__(self, controller: TrainController_Tot_Container):
        super().__init__()
        self.business_logic = TrainBusinessLogic()
        self.train_dict = self.business_logic.train_dict
        self.controller = controller

    @pyqtSlot(dict, dict, bool, int, dict)
    def update_train_model_from_track_model(self, auth_speed_dict: dict, block_dict: dict, new_train: bool,
                                            remove_train: int, passenger_dict: dict):
        
        print("Train Model: reached update_train_model_from_track_model\n")
        self.business_logic.passenger_return.clear()
        self.business_logic.delta_x_return.clear()
        if remove_train in self.train_dict.keys():
            self.remove_train(remove_train)

        if new_train:
            self.add_train()

        for i in auth_speed_dict.keys():
            speed = auth_speed_dict[i][1]
            auth = auth_speed_dict[i][0]
            self.track_model_inputs([speed, auth], i)

        for i in block_dict.keys():
            self.track_update_block(block_dict[i], i)

        for key, value in passenger_dict.items():
            if not (value <= 0):
                self.track_update_passengers(value, key)

        self.business_logic.train_update_controller()

        print("Train Model Container: train_update_controller successful")

        self.physics_calculation()

        self.update_track_model_from_train_model.emit(self.business_logic.delta_x_return,
                                                      self.business_logic.passenger_return)

    def track_model_inputs(self, input_list, index):
        print("Train Model Container: train's track model inputs hit \n")

        print(f"Train Model Container: track_model_inputs: {index}, {input_list}")

        # the list provided should have entries in this order: [commanded speed, vital authority]
        self.train_dict = self.business_logic.train_dict
        if len(self.train_dict) == 0:
            return
        elif not (index in self.train_dict.keys()):
            return
        else:
            self.business_logic.track_model_inputs(input_list, index)
            self.train_dict = self.business_logic.train_dict

    def train_controller_inputs(self, input_list, index):
        print("Train model Container: train_controller_inputs called")
        # the list provided should have the entries in this order: [commanded speed, power, service brake,
        # emergency brake, left/right doors, announce station, cabin lights, headlights]
        self.train_dict = self.business_logic.train_dict
        if len(self.train_dict) == 0:
            return
        if not (index in self.train_dict.keys()):
            return
        else:
            self.business_logic.train_controller_inputs(input_list, index)

    def track_update_block(self, block_vals, index):
        # block_vals should be a list as such: [grade, elevation, underground, beacon]
        self.train_dict = self.business_logic.train_dict
        if len(self.train_dict) == 0:
            return
        if not (index in self.train_dict.keys()):
            return
        self.business_logic.track_update_block(block_vals, index)
        self.train_dict = self.business_logic.train_dict
        print('Train Model Container:track_update_block passed')

    def track_update_passengers(self, num, index):
        self.train_dict = self.business_logic.train_dict
        if len(self.train_dict) == 0:
            return
        if not (index in self.train_dict.keys()):
            return
        try:
            self.business_logic.track_update_passengers(num, index)
        except Exception as error:
            print("Train Model Container: ", error)
        self.train_dict = self.business_logic.train_dict

    def controller_update_temp(self, num, index):
        self.train_dict = self.business_logic.train_dict
        if len(self.train_dict) == 0:
            return
        if not (index in self.train_dict.keys()):
            return
        self.business_logic.controller_update_temp(num, index)

    def physics_calculation(self):
        self.business_logic.physics_calculation()

    def add_train(self):
        print("Train Model Container: add train endpoint hit\n")
        self.business_logic.add_train(self.controller)
        print("Train Model Container: train added in train container")

    def remove_train(self, index):
        print("Train Model Container: train remove hit\n")
        self.business_logic.remove_train(index)
        print("Train Model Container: train removed from container")

    def show_ui(self):
        self.ui = UITrain(self.business_logic)
        self.ui.show()

import sys

from PyQt6.QtCore import QObject, pyqtSignal
from PyQt6.QtWidgets import QApplication

from Train_Model import TrainBusinessLogic, UITrain
from trainControllerTot_Container import TrainController_Tot_Container
from SystemTime import SystemTimeContainer


class TrainModelContainer(QObject):
    update_track_model_from_train_model = pyqtSignal(object, list)

    def __init__(self, controller: TrainController_Tot_Container, time: SystemTimeContainer):
        super().__init__()
        self.business_logic = TrainBusinessLogic(time)
        self.train_dict = self.business_logic.train_dict
        self.controller = controller
        self.controller.new_train_values_signal.connect(self.train_controller_inputs)
        self.controller.new_train_temp_signal.connect(self.controller_update_temp)

    def update_train_model_from_track_model(self, auth_speed_list: list, block_dict: dict, new_train: bool,
                                            remove_train: int, passenger_list: list):
        self.business_logic.passenger_return.clear()
        self.business_logic.delta_x_return.clear()

        if remove_train in self.train_dict.keys():
            self.remove_train(remove_train)

        if new_train:
            self.add_train()

        for entry in auth_speed_list:
            self.track_model_inputs([entry[2], entry[1]], entry[0])

        for i in block_dict.keys():
            self.track_update_block(block_dict[i], i)

        for entry in passenger_list:
            if not (entry[1] <= 0):
                self.track_update_passengers(entry[1], entry[0])

        self.physics_calculation()

        disembarking_passengers_update = list()
        for i in self.business_logic.passenger_return.keys():
            disembarking_passengers_update.append((i, self.business_logic.passengers_updated[i]))

        self.update_track_model_from_train_model.emit(self.business_logic.delta_x_return,
                                                      disembarking_passengers_update)


    def track_model_inputs(self, input_list, index):
        print("train's track model inputs hit")

        print(f"track_model_inputs: {index}, {input_list}")

        # the list provided should have entries in this order: [commanded speed, vital authority]
        self.train_dict = self.business_logic.train_dict
        if len(self.train_dict) == 0:
            return
        elif not (index in self.train_dict.keys()):
            return
        else:
            self.business_logic.track_model_inputs(input_list, index)
            self.train_dict = self.business_logic.train_dict
            self.controller.getvaluesfromtrain_update1([self.train_dict[index].signals.authority,
                                                        self.train_dict[index].signals.commanded_speed, ])

    def train_controller_inputs(self, input_list, index):
        print("Train model: train_controller_inputs called")
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
        self.controller.getvaluesfromtrain_update2([self.train_dict[index].track_circuit,
                                                    self.train_dict[index].underground,
                                                    self.train_dict[index].signals.beacon])
        print('track_update_block passed')

    def track_update_passengers(self, num, index):
        self.train_dict = self.business_logic.train_dict
        if len(self.train_dict) == 0:
            return
        if not (index in self.train_dict.keys()):
            return
        self.business_logic.passengers_updated(num, index)
        self.train_dict = self.business_logic.train_dict
        self.controller.getvaluesfromtrain_update2([self.train_dict[index].track_circuit,
                                                    self.train_dict[index].new_block.underground,
                                                    self.train_dict[index].signals.beacon])

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
        print("train endpoint hit")
        self.business_logic.add_train(self.controller)
        print("train added in train container")

    def remove_train(self, index):
        self.business_logic.train_removed(index)

    def show_ui(self):
        app = QApplication.instance()

        if app is None:
            app = QApplication([])

        self.ui = UITrain(self.business_logic)
        self.ui.show()

        app.exec()

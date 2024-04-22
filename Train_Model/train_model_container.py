from PyQt6.QtCore import QObject, pyqtSignal, pyqtSlot

from Train_Model.train_model_signals import train_model_signals
from TopLevelSignals import TopLevelSignals
from Train_Model.business_logic import train_business_logic


class TrainModelContainer(QObject):
    update_track_model_from_train_model = pyqtSignal(object, object)

    def __init__(self):
        super().__init__()
        self.signals = train_model_signals
        self.signals.business_update.connect(self.return_to_track_model)
        self.signals.tb_track_model_inputs.connect(self.track_model_inputs)
        self.signals.tb_add_train.connect(self.add_train)
        self.signals.tb_remove_train.connect(self.remove_train)
        self.signals.tb_train_controller_inputs.connect(self.train_controller_inputs)
        self.signals.tb_physics_calculation.connect(self.physics_calculation)
        self.signals.tb_track_update_block.connect(self.track_update_block)
        self.signals.tb_controller_update_temp.connect(self.controller_update_temp)
        self.signals.tb_train_controller_inputs.connect(self.train_controller_inputs)
        self.signals.tb_track_update_passenger.connect(self.track_update_passengers)
        self.top_signal = TopLevelSignals
        self.top_signal.update_train_model_from_track_model.connect(self.update_train_model_from_track_model)

    @pyqtSlot(dict, dict, bool, int, dict)
    def update_train_model_from_track_model(self, auth_speed_dict: dict, block_dict: dict, new_train: bool,
                                            remove_train: int, passenger_dict: dict):
        
        print("Train Model: reached update_train_model_from_track_model\n")
        self.signals.clear_return_dicts.emit()

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

        self.signals.train_update_controller.emit()

        print("Train Model Container: train_update_controller successful")

        self.physics_calculation()

        self.signals.send_back_track_returns.emit()

    @pyqtSlot(dict, dict)
    def return_to_track_model(self, delta_x_return: dict, passenger_return: dict):
        self.top_signal.update_track_model_from_train_model.emit(delta_x_return, passenger_return)

    @pyqtSlot(tuple, int)
    def track_model_inputs(self, input_list, index):
        print("Train Model Container: train's track model inputs hit \n")

        print(f"Train Model Container: track_model_inputs: {index}, {input_list}")

        # the list provided should have entries in this order: [commanded speed, vital authority]
        input_list = tuple(input_list)
        self.signals.track_model_inputs.emit(input_list, index)

    @pyqtSlot(tuple, int)
    def train_controller_inputs(self, input_list, index):
        print("Train model Container: train_controller_inputs called")
        # the list provided should have the entries in this order: [commanded speed, power, service brake,
        # emergency brake, left/right doors, announce station, cabin lights, headlights]
        input_list = tuple(input_list)
        self.signals.train_controller_inputs.emit(input_list, index)

    @pyqtSlot(tuple, int)
    def track_update_block(self, block_vals, index):
        # block_vals should be a list as such: [grade, elevation, underground, beacon]
        block_vals = tuple(block_vals)
        self.signals.track_update_block.emit(block_vals, index)
        print('Train Model Container:track_update_block passed')

    @pyqtSlot(int, int)
    def track_update_passengers(self, num, index):
        self.signals.track_update_passenger.emit(num, index)

    @pyqtSlot(float, int)
    def controller_update_temp(self, num, index):
        self.signals.controller_update_temp.emit(num, index)

    @pyqtSlot()
    def physics_calculation(self):
        self.signals.physics_calculation.emit()

    @pyqtSlot()
    def add_train(self):
        print("Train Model Container: add train endpoint hit\n")
        self.signals.business_add_train.emit()
        print("Train Model Container: train added in train container")

    @pyqtSlot(int)
    def remove_train(self, index):
        print("Train Model Container: train remove hit\n")
        self.signals.business_remove_train.emit(index)
        print("Train Model Container: train removed from container")

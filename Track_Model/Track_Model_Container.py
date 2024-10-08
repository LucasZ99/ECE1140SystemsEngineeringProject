import os
import sys

from PyQt6.QtCore import QObject, pyqtSignal
from PyQt6.QtWidgets import QApplication
from pandas.io.formats import console

from Track_Model.Track_Model import TrackModel
from Track_Model.Track_Model_UI import Window

from TopLevelSignals import TopLevelSignals as top_level_signals
from Track_Model.TrackModelSignals import TrackModelSignals as signals


class TrackModelContainer(QObject):

    # Signals to launcher
    # update_train_model_from_track_model = pyqtSignal(object, object, bool, int, object)
    # update_ctc_from_track_model = pyqtSignal(int)
    # update_wayside_from_track_model = pyqtSignal(object)

    # Signals from track_model
    # new_block_occupancy_signal = pyqtSignal(list)
    # new_ticket_sales_signal = pyqtSignal(int)
    # refresh_ui_signal = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.track_model = TrackModel("Green Line.xlsx")
        self.top_level_signals = top_level_signals
        self.signals = signals

        # Connect Track Model Signals to UI Slots:
        # self.signals.refresh_ui_signal.connect(self.refresh_ui)
        # self.signals.map_add_train_signal.connect(self.map_add_train)
        # self.signals.map_move_train_signal.connect(self.map_move_train)
        #
        # self.signals.get_data_signal.connect(self.get_data_from_track_model)
        # self.signals.get_block_info_signal.connect(self.get_block_info_from_track_model)
        # self.signals.get_train_dict_signal.connect(self.get_train_dict_from_track_model)

        # Connect UI Signals to Track Model Slots:
        self.signals.set_power_failure_signal.connect(self.set_track_model_power_failure)
        self.signals.set_track_circuit_failure_signal.connect(self.set_track_model_track_circuit_failure)
        self.signals.set_broken_rail_failure_signal.connect(self.set_track_model_broken_rail_failure)

        self.signals.set_env_temperature_signal.connect(self.set_track_model_env_temperature)
        self.signals.set_heaters_signal.connect(self.set_track_model_heaters)

        # Connect Top Level Signals
        self.top_level_signals.update_track_model_from_wayside.connect(self.update_track_model_from_wayside)
        self.top_level_signals.update_track_model_from_train_model.connect(self.update_track_model_from_train_model)
        self.top_level_signals.maintenance_mode_update.connect(self.set_infrastructure)

    # show ui
    # def show_ui(self):
    #     # app = QApplication.instance()  # Get the QApplication instance
    #     #
    #     # # app_flag = False
    #     # if app is None:
    #     #     app = QApplication([])  # If QApplication instance doesn't exist, create a new one
    #     #    # app_flag = True
    #
    #     self.track_model_ui.show()
    #
    #     # # if app_flag is True:
    #     # app.exec()

    # endpoints

    # Track Controller

    # Receiving inputs


    # def update_authority(self, authority: list[int]):
    #     print('track model update authority called')
    #     self.track_model.update_authority(authority)  # update our track model object
    #     print(f'yard block authority track model is using: {authority[61]}')
    #     if authority[61]:
    #         self.train_model_container.add_train()
    #     print(f'track model got this authority from controller: {authority}')
    #     print(f'track model is giving train model speed = {self.track_model.get_tm_speed(1)}, authority = {self.track_model.get_tm_authority(1)}')
    #     self.train_model_container.track_model_inputs(
    #         [self.track_model.get_tm_speed(1), self.track_model.get_tm_authority(1)], 1)  # send new info to train model
    #
    # def update_speed(self, speed: list[float]):
    #     print('update speed called')
    #     self.track_model.update_speed(speed)  # update our track model object
    #     print(f'track model got this speed from controller: {speed}')
    #     print(f'track model is giving train model speed = {self.track_model.get_tm_speed(1)}, authority = {self.track_model.get_tm_authority(1)}')
    #     self.train_model_container.track_model_inputs(
    #         [self.track_model.get_tm_speed(1), self.track_model.get_tm_authority(1)], 1)  # send new info to train model


    # def toggle_switch(self, block_id: int):
    #     print('toggle switch called')
    #     self.track_model.toggle_switch(block_id)
    #     self.track_model_ui.refresh()
    #
    # def toggle_signal(self, block_id: int):
    #     print('toggle signal called')
    #     self.track_model.toggle_signal(block_id)
    #     self.track_model_ui.refresh()
    #
    # def toggle_crossing(self, block_id: int):
    #     print('toggle crossing called')
    #     self.track_model.toggle_crossing(block_id)
    #     self.track_model_ui.refresh()
    #
    # def open_block(self, block_id: int):
    #     print('open block called')
    #     self.track_model.open_block(block_id)
    #     self.track_model_ui.refresh()
    #
    # def close_block(self, block_id: int):
    #     print('close block called')
    #     self.track_model.close_block(block_id)
    #     self.track_model_ui.refresh()

        # Emitting signals

    # def new_block_occupancy(self, block_occupancy: list[bool]):
    #     print('new block occupancy called from track model container')
    #     self.new_block_occupancy_signal.emit(block_occupancy)
    #     print('track model passed')
    #
    # def new_ticket_sales(self, ticket_sales: int):
    #     print('new ticket sales called from track model container')
    #     self.new_ticket_sales_signal.emit(ticket_sales)

    # Train Model

    # Catching signals
    # def train_spawned(self, index):
    #     print('train spawned called from track model container')
    #     self.track_model.train_spawned()
    #     self.train_model_container.track_update_block([
    #         self.track_model.get_tm_grade(index),
    #         self.track_model.get_tm_elevation(index),
    #         self.track_model.get_tm_block_length(index),
    #         self.track_model.get_tm_underground_status(index),
    #         self.track_model.get_tm_beacon(index)
    #     ], index)

    # def train_presence_changed(self, index):
    #     print('train presence changed called')
    #     self.track_model.train_presence_changed(1)  # train id=1 for IT3
    #     self.train_model_container.track_update_block([])
    #     self.train_model_container.track_update_block([
    #         self.track_model.get_tm_grade(index),
    #         self.track_model.get_tm_elevation(index),
    #         self.track_model.get_tm_block_length(index),
    #         self.track_model.get_tm_underground_status(index),
    #         self.track_model.get_tm_beacon(index)
    #     ], index)
    #     self.train_model_container.track_model_inputs(
    #         [self.track_model.get_tm_speed(1), self.track_model.get_tm_authority(1)], 1)

    # def refresh_ui(self):
    #     self.signals.refresh_ui_signal.emit()

    def update_track_model_from_wayside(self, authority_safe_speed_update, switch_changed_indexes,
                                        signal_changed_indexes, rr_crossing_indexes, toggle_block_indexes):
        print('Track Model: update_track_model_from_wayside called')
        add_train = False  # default
        remove_train = self.track_model.get_remove_train()
        print('Track Model: updating self.track_model infrastructure')
        self.track_model.update_infrastructure(switch_changed_indexes, signal_changed_indexes, rr_crossing_indexes,
                                               toggle_block_indexes)
        # update infrastructure on map
        for index, value in signal_changed_indexes:
            print(f'track model container: {index}, {value}')
            self.signals.map_update_signal_signal.emit(index, value)
        for index, value in rr_crossing_indexes:
            self.signals.map_update_rxr_signal.emit(index, value)
        closed_blocks = self.track_model.get_closure_dict()
        for index in toggle_block_indexes:
            self.signals.map_update_closure_signal.emit(index, closed_blocks[index])
        # update track_model
        print('Track Model: updating self.track_model authority and speed')
        self.track_model.update_authority_and_safe_speed(authority_safe_speed_update)
        # check if we should spawn a new train (authority @ 62 = nonzero & no train on 62)
        print('Track Model: check if we should spawn a new train')
        for i in range(0, len(authority_safe_speed_update)):
            block_id = authority_safe_speed_update[i][0]
            authority = authority_safe_speed_update[i][1]
            safe_speed = authority_safe_speed_update[i][2]
            if block_id == 62 and authority > 0:
                train_on_yard = False
                for key, val in self.track_model.get_train_dict().items():
                    if val == 62:
                        train_on_yard = True
                if not train_on_yard:
                    # spawn train
                    add_train = True
                    self.track_model.train_spawned()
        train_dict = self.track_model.get_train_dict()  # copy train dict

        # check for embarking passengers at station
        embarking_passengers_update = self.track_model.get_embarking_passengers()
        print(f'Track Model: embarking_passengers_update = {embarking_passengers_update}')
        # change authority_safe_speed_update to be train based instead of block based
        # list[tuple[block_id: int, authority: int, safe_speed: float]] ->
        # dict[train_id:int, (authority: int, safe_speed: float)]
        print('Track Model: change authority_safe_speed_update to be train based instead of block based')
        authority_dict = self.track_model.get_authority_dict()
        speed_dict = self.track_model.get_speed_dict()
        authority_safe_speed_dict = {}
        for key, value in train_dict.items():
            authority_safe_speed_dict[key] = (authority_dict[value], speed_dict[value])
        print(f'authority_safe_speed_update: {authority_safe_speed_update}')
        print(f'authority_safe_speed_dict: {authority_safe_speed_dict}')
        # get new block info from track_model for each train
        print('Track Model: get new block info from track_model for each train')
        block_info_dict = {}
        for key in train_dict:
            block_info_dict[key] = self.track_model.get_block_info_for_train(key)
        # emit
        self.signals.refresh_ui_signal.emit()  # pre-emit ui refresh
        print('Track Model: emitting update_train_model_from_track_model')
        self.top_level_signals.update_train_model_from_track_model.emit(authority_safe_speed_dict, block_info_dict,
                                                                        add_train,
                                                                        remove_train, embarking_passengers_update)

    def update_track_model_from_train_model(self, delta_x_dict, disembarking_passengers_dict):
        print('Track Model: update_track_model_from_train_model called')
        print('delta_x_dict: ', delta_x_dict)
        # TODO: disembarking passengers
        # for each train, calculate current block given delta x
        # update our track model train dict (train will get block info in next downstream)
        self.track_model.update_delta_x_dict(delta_x_dict)
        # update map on ui handled by signals emitted by track_model
        ticket_sales = 0  # TODO: implement ticket sales for ctc
        # block_occupancy_update = dict(enumerate(self.track_model.get_occupancy_list(), 1))  # old way, 1-->150
        block_occupancy_update = {i: v for i, v in enumerate(self.track_model.get_occupancy_list(), 1) if
                                  i <= 57 or i >= 62}

        # emit
        self.signals.refresh_ui_signal.emit()  # pre-emit ui refresh
        print('Track Model: emitting update_ctc_from_track_model')
        self.top_level_signals.update_ctc_from_track_model.emit(ticket_sales)
        print('Track Model: emitting update_wayside_from_track_model')
        # print(f'Track Model: block_occupancy_update = {block_occupancy_update}')
        self.top_level_signals.update_wayside_from_track_model.emit(block_occupancy_update)

    #
    # Connect Signals to Slots:
    #

    def map_add_train(self):
        print('Track Model Container: map_add_train called')
        self.signals.map_add_train_signal.emit()

    def map_move_train(self, train_id, block):
        self.signals.map_move_train_signal.emit(train_id, block)

    def get_data_from_track_model(self):
        return self.track_model.get_data()

    def get_block_info_from_track_model(self, block_id):
        return self.track_model.get_block_info(block_id)

    def get_train_dict_from_track_model(self):
        return self.track_model.get_train_dict()

    def set_track_model_power_failure(self, block_id, val):
        self.track_model.set_power_failure(block_id, val)

    def set_track_model_track_circuit_failure(self, block_id, val):
        self.track_model.set_track_circuit_failure(block_id, val)

    def set_track_model_broken_rail_failure(self, block_id, val):
        self.track_model.set_broken_rail_failure(block_id, val)

    def set_track_model_env_temperature(self, temp):
        self.track_model.set_env_temperature(temp)

    def set_track_model_heaters(self, val):
        self.track_model.set_heaters(val)

    def set_infrastructure(self, switch_list, signal_list):
        # print('Track Model Container: update_infrastructure called')
        # print(f'Track Model Container: signal_list: {signal_list}')
        # self.track_model.update_infrastructure(switch_list, signal_list)
        # self.track_model_ui.refresh()
        self.track_model.update_infrastructure(switch_list, signal_list, [],
                                               [])
        # maybe refresh here
        # update infrastructure on map TODO: Update map straight from track model
        for index, value in signal_list:
            self.signals.map_update_signal_signal.emit(index, value)

        self.signals.refresh_ui_signal.emit()






import os
import sys

# TODO: one signal in and out, connected at head level

from PyQt6.QtCore import QObject, pyqtSignal
from PyQt6.QtWidgets import QApplication

from Track_Model.Track_Model import TrackModel
from Track_Model.Track_Model_UI import Window


class TrackModelContainer(QObject):

    # Signals to launcher
    update_train_model_from_track_model = pyqtSignal(object, object, bool, int, object)
    update_ctc_from_track_model = pyqtSignal(int)
    update_wayside_from_track_model = pyqtSignal(object)

    # Signals from track_model
    # new_block_occupancy_signal = pyqtSignal(list)
    # new_ticket_sales_signal = pyqtSignal(int)
    # refresh_ui_signal = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.track_model = TrackModel("./Track_Model/Green Line.xlsx")
        self.track_model_ui = Window(self.track_model)

        # connect internal signals (from object)
        # self.track_model.new_block_occupancy_signal.connect(self.new_block_occupancy)
        # self.track_model.new_ticket_sales_signal.connect(self.new_ticket_sales)
        # self.track_model.refresh_ui_signal.connect(self.refresh_ui)
        # connect external signal


    # show ui
    def show_ui(self):
        app = QApplication.instance()  # Get the QApplication instance

        # app_flag = False
        if app is None:
            app = QApplication([])  # If QApplication instance doesn't exist, create a new one
            # app_flag = True

        self.track_model_ui.show()

        # if app_flag is True:
        app.exec()

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

    def refresh_ui(self):
        self.track_model_ui.refresh()

    def update_track_model_from_wayside(self, authority_safe_speed_update):
        print('Track Model: update_track_model_from_wayside called')
        # print(f'authority_safe_speed_update: {authority_safe_speed_update}')
        add_train = False  # default
        remove_train = self.track_model.get_remove_train()
        embarking_passengers_update = {}  # TODO: implement embarking passengers dict per train
        # update track_model
        print('Track Model: updating self.track_model')
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
        # TODO: implement removing trains (on way up maybe)
        train_dict = self.track_model.get_train_dict()  # copy train dict

        # change authority_safe_speed_update to be train based instead of block based
        # list[tuple[block_id: int, authority: int, safe_speed: float]] ->
        # dict[train_id:int, (authority: int, safe_speed: float)]
        print('Track Model: change authority_safe_speed_update to be train based instead of block based')
        authority_safe_speed_list = [list(t) for t in authority_safe_speed_update]
        for i in range(0, len(authority_safe_speed_list)):
            block_id = authority_safe_speed_list[i][0]
            for key, val in train_dict.items():  # train_id, block
                if val == block_id:
                    authority_safe_speed_list[i][0] = key
        authority_safe_speed_dict = {lst[0]: lst[1:] for lst in authority_safe_speed_list}
        print(f'authority_safe_speed_update: {authority_safe_speed_list}')
        print(f'authority_safe_speed_dict: {authority_safe_speed_dict}')
        # get new block info from track_model for each train
        print('Track Model: get new block info from track_model for each train')
        block_info_dict = {}
        for key in train_dict:
            block_info_dict[key] = self.track_model.get_block_info_for_train(key)
        # emit
        self.track_model_ui.refresh()  # pre-emit ui refresh
        print('Track Model: emitting update_train_model_from_track_model')
        self.update_train_model_from_track_model.emit(authority_safe_speed_dict, block_info_dict, add_train,
                                                      remove_train, embarking_passengers_update)

    def update_track_model_from_train_model(self, delta_x_dict, disembarking_passengers_update):
        print('Track Model: update_track_model_from_train_model called')
        print('delta_x_dict: ', delta_x_dict)
        # TODO: disembarking passengers
        # for each train, calculate current block given delta x
        # update our track model train dict (train will get block info in next downstream)
        self.track_model.update_delta_x_dict(delta_x_dict)
        ticket_sales = 0  # TODO: implement ticket sales for ctc
        block_occupancy_update = dict(enumerate(self.track_model.get_occupancy_list(), 1))

        # emit
        self.track_model_ui.refresh()  # pre-emit ui refresh
        print('Track Model: emitting update_ctc_from_track_model')
        self.update_ctc_from_track_model.emit(ticket_sales)
        print('Track Model: emitting update_wayside_from_track_model')
        print(f'Track Model: block_occupancy_update = {block_occupancy_update}')
        self.update_wayside_from_track_model.emit(block_occupancy_update)

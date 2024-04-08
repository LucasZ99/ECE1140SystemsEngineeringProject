import os
import sys

# TODO: one signal in and out, connected at head level

from PyQt6.QtCore import QObject, pyqtSignal
from PyQt6.QtWidgets import QApplication

from Track_Model.Track_Model import TrackModel
from Track_Model.Track_Model_UI import Window


class TrackModelContainer(QObject):

    # Signals
    update_train_model_from_track_model = pyqtSignal(list, list, bool)
    update_ctc_from_track_model = pyqtSignal(int)
    # new_block_occupancy_signal = pyqtSignal(list)
    # new_ticket_sales_signal = pyqtSignal(int)

    def __init__(self):
        super().__init__()
        self.track_model = TrackModel("./Track_Model/Green Line.xlsx")
        self.track_model_ui = Window(self.track_model)

        # connect internal signals (from object)
        self.track_model.new_block_occupancy_signal.connect(self.new_block_occupancy)
        self.track_model.new_ticket_sales_signal.connect(self.new_ticket_sales)
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
    # TODO: every time train enters new block also update authority/speed
    def update_authority(self, authority: list[int]):
        print('track model update authority called')
        self.track_model.update_authority(authority)  # update our track model object
        print(f'yard block authority track model is using: {authority[61]}')
        if authority[61]:
            self.train_model_container.add_train()
        print(f'track model got this authority from controller: {authority}')
        print(f'track model is giving train model speed = {self.track_model.get_tm_speed(1)}, authority = {self.track_model.get_tm_authority(1)}')
        self.train_model_container.track_model_inputs(
            [self.track_model.get_tm_speed(1), self.track_model.get_tm_authority(1)], 1)  # send new info to train model

    def update_speed(self, speed: list[float]):
        print('update speed called')
        self.track_model.update_speed(speed)  # update our track model object
        print(f'track model got this speed from controller: {speed}')
        print(f'track model is giving train model speed = {self.track_model.get_tm_speed(1)}, authority = {self.track_model.get_tm_authority(1)}')
        self.train_model_container.track_model_inputs(
            [self.track_model.get_tm_speed(1), self.track_model.get_tm_authority(1)], 1)  # send new info to train model

    def toggle_switch(self, block_id: int):
        print('toggle switch called')
        self.track_model.toggle_switch(block_id)
        self.track_model_ui.refresh()

    def toggle_signal(self, block_id: int):
        print('toggle signal called')
        self.track_model.toggle_signal(block_id)
        self.track_model_ui.refresh()

    def toggle_crossing(self, block_id: int):
        print('toggle crossing called')
        self.track_model.toggle_crossing(block_id)
        self.track_model_ui.refresh()

    def open_block(self, block_id: int):
        print('open block called')
        self.track_model.open_block(block_id)
        self.track_model_ui.refresh()

    def close_block(self, block_id: int):
        print('close block called')
        self.track_model.close_block(block_id)
        self.track_model_ui.refresh()

        # Emitting signals

    def new_block_occupancy(self, block_occupancy: list[bool]):
        print('new block occupancy called from track model container')
        self.new_block_occupancy_signal.emit(block_occupancy)
        print('track model passed')

    def new_ticket_sales(self, ticket_sales: int):
        print('new ticket sales called from track model container')
        self.new_ticket_sales_signal.emit(ticket_sales)

    # Train Model

    # Catching signals
    def train_spawned(self, index):
        print('train spawned called from track model container')
        self.track_model.train_spawned()
        self.train_model_container.track_update_block([
            self.track_model.get_tm_grade(index),
            self.track_model.get_tm_elevation(index),
            self.track_model.get_tm_block_length(index),
            self.track_model.get_tm_underground_status(index),
            self.track_model.get_tm_beacon(index)
        ], index)

    def train_presence_changed(self, index):
        print('train presence changed called')
        self.track_model.train_presence_changed(1)  # train id=1 for IT3
        self.train_model_container.track_update_block([])
        self.train_model_container.track_update_block([
            self.track_model.get_tm_grade(index),
            self.track_model.get_tm_elevation(index),
            self.track_model.get_tm_block_length(index),
            self.track_model.get_tm_underground_status(index),
            self.track_model.get_tm_beacon(index)
        ], index)
        self.train_model_container.track_model_inputs(
            [self.track_model.get_tm_speed(1), self.track_model.get_tm_authority(1)], 1)  # send new info to train model

    def update_track_model_from_wayside(self, authority_safe_speed_update):
        # update track model

        # update train_model
        # TODO
        # change authority_safe_speed_update to be train based instead of block based
        # TODO
        # get new block info from track_model for each train
        train_dict = self.train_model.get_train_dict()
        block_info_dict = {}
        for key in train_dict:
            block_info_dict[key] = self.track_model.get_block_info_for_train(key)
        self.update_train_model_from_track_model.emit(authority_safe_speed_update, block_info_dict)

    def update_track_model_from_train_model(self):
        pass

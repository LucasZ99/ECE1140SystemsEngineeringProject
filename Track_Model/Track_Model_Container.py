import os
import sys

from PyQt6.QtCore import QObject, pyqtSignal, pyqtSlot
from PyQt6.QtWidgets import QApplication

from Track_Model.Track_Model import TrackModel
from Track_Model.Track_Model_UI import Window
from Train_Model import TrainModelContainer


class TrackModelContainer(QObject):

    # Signals
    # Upstream
    update_wayside_from_track_model = pyqtSignal(dict[int, bool])


    new_block_occupancy_signal = pyqtSignal(list)
    new_ticket_sales_signal = pyqtSignal(int)

    def __init__(self, train_model_container: TrainModelContainer):
        super().__init__()
        self.train_model_container = train_model_container

        self.track_model = TrackModel("./Track_Model/Green Line.xlsx")
        self.track_model_ui = Window(self.track_model)

        # connect internal signals
        self.track_model.new_block_occupancy_signal.connect(self.new_block_occupancy)
        self.track_model.new_ticket_sales_signal.connect(self.new_ticket_sales)
        # connect external signals
        self.train_model_container.new_train_added.connect(self.train_spawned)
        self.train_model_container.train_enters_new_block.connect(self.train_presence_changed)

    @pyqtSlot(list, list, list, list, list)
    def update_track_model_from_wayside(self,
                                        authority_safe_speed_update: list[tuple[int, int, float]],
                                        switch_changed_indexes: list[int],
                                        signal_changed_indexes: list[int],
                                        rr_crossing_indexes: list[int],
                                        toggle_block_indexes: list[int]):
        pass

    # show ui
    def show_ui(self):
        app = QApplication.instance()  # Get the QApplication instance

        # app_flag = False
        if app is None:
            app = QApplication([])  # If QApplication instance doesn't exist, create a new one
            # app_flag = True

        print("before ui show")
        self.track_model_ui.show()
        print("After ui show")

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

        print(f'track model is giving train model speed = {self.track_model.get_tm_speed(1)}, authority = {self.track_model.get_tm_authority(1)}')
        self.train_model_container.track_model_inputs(
            [self.track_model.get_tm_speed(1), self.track_model.get_tm_authority(1)], 1)  # send new info to train model

    def update_speed(self, speed: list[float]):
        print('update speed called')
        self.track_model.update_speed(speed)  # update our track model object
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

    # Sending outputs are done any time we get new authority/speed or enter a new block

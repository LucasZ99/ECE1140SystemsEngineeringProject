import os
import sys

from PyQt6.QtCore import QObject, pyqtSignal
from PyQt6.QtWidgets import QApplication

from Track_Model.Track_Model import TrackModel
from Track_Model.Track_Model_UI import Window


class TrackModelContainer(QObject):

    # Signals
    new_block_occupancy_signal = pyqtSignal(list)
    new_ticket_sales_signal = pyqtSignal(int)

    def __init__(self):
        super().__init__()
        self.track_model = TrackModel("./Track_Model/Green Line.xlsx")
        self.track_model_ui = Window(self.track_model)

        # connect internal signals
        self.track_model.new_block_occupancy_signal.connect(self.new_block_occupancy)
        self.track_model.new_ticket_sales_signal.connect(self.new_ticket_sales)
        # connect external signals
        # self.train_model.signal.connect(self.function)
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

    def update_authority(self, authority: list[int]):
        print('update authority called')
        self.track_model.update_authority(authority)
        # TODO: Add refresh UI

    def update_speed(self, speed: list[float]):
        print('update speed called')
        self.track_model.update_speed(speed)

    def toggle_switch(self, block_id: int):
        print('toggle switch called')
        self.track_model.toggle_switch(block_id)

    def toggle_signal(self, block_id: int):
        print('toggle signal called')
        self.track_model.toggle_signal(block_id)

    def toggle_crossing(self, block_id: int):
        print('toggle crossing called')
        self.track_model.toggle_crossing(block_id)

    def open_block(self, block_id: int):
        print('open block called')
        self.track_model.open_block(block_id)

    def close_block(self, block_id: int):
        print('close block called')
        self.track_model.close_block(block_id)

        # Emitting signals

    def new_block_occupancy(self, block_occupancy: list[bool]):
        print('new block occupancy called from track model container')
        self.new_block_occupancy_signal.emit(block_occupancy)

    def new_ticket_sales(self, ticket_sales: int):
        print('new ticket sales called from track model container')
        self.new_ticket_sales_signal.emit(ticket_sales)
    # Train Model

    # Catching signals

    # Sending outputs

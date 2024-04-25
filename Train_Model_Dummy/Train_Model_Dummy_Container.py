import os
import sys

from PyQt6.QtCore import QObject, pyqtSignal, pyqtSlot
from PyQt6.QtWidgets import QApplication
from pandas.io.formats import console
from SystemTime import SystemTime

from TopLevelSignals import TopLevelSignals as top_level_signals


class TrainModelContainerDummy(QObject):  # Note, this can just hold all the logic, just named container for convention

    def __init__(self):
        super().__init__()
        self.top_level_signals = top_level_signals
        # Connect Top Level Signals
        self.top_level_signals.update_train_model_from_track_model.connect(self.update_train_model_from_track_model)
        self.train_dict = {}  # this will hold trains and delta_x (is essentially our delta_x_dict)
        self.train_count = 0
        self.passenger_count = 0
        self.previous_time = SystemTime.time()

    @pyqtSlot(dict, dict, bool, bool, int)
    def update_train_model_from_track_model(self,
                                            authority_safe_speed_dict: dict,   # {Train_ID : (authority, speed)}
                                            block_info_dict: dict,             # {Train_ID : (block info tuple)}
                                            add_train: bool,                   # Bool for adding trains
                                            remove_train: bool,                # index of train to remove or -1
                                            embarking_passengers_update: dict  # {Train_ID: embarking_passengers}
                                            ):

        self.update_delta_x(authority_safe_speed_dict)
        disembarking_passengers_dict = {}  # Formatted {Train_ID: disembarking_passengers, disembarking_passenger}

        # if add_train, add a train to dictionary
        if add_train:
            self.add_train()
        # if remove_train != -1, remove train from dictionary at that index
        if remove_train != -1:
            self.remove_train(remove_train)

        # TODO: update delta x from authority_safe_speed_dict and time-lapsed
        self.update_delta_x(authority_safe_speed_dict)
        # pretty irrelevant: maybe a UI could display block_info_dict

        # pretty irrelevant: update passenger count from embarking_passengers_update
        # pretty irrelevant: generate disembarking passengers when at station

        # End by emitting back to track_model
        self.top_level_signals.update_track_model_from_train_model.emit(self.train_dict, disembarking_passengers_dict)

    def add_train(self):
        self.train_count += 1
        self.train_dict[self.train_count] = 0

    def remove_train(self, index):
        del self.train_dict[index]
        self.train_count -= 1

    def update_delta_x(self, authority_safe_speed_dict: dict):
        i = 1
        for train in self.train_dict:
            self.train_dict[i] += self.calc_delta_x(authority_safe_speed_dict[i])
            i += 1

        self.previous_time = SystemTime.time()

    def calc_delta_x(self, authority_safe_speed: tuple) -> float:
        if authority_safe_speed[0] != 0 and authority_safe_speed[1] != 0:
            return authority_safe_speed[1] * (SystemTime.time() - self.previous_time)
        else:
            return 0

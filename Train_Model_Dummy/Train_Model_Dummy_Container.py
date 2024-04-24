import os
import sys

from PyQt6.QtCore import QObject, pyqtSignal
from PyQt6.QtWidgets import QApplication
from pandas.io.formats import console

from TopLevelSignals import TopLevelSignals as top_level_signals


class TrainModelContainerDummy(QObject):  # Note, this can just hold all the logic, just named container for convention

    def __init__(self):
        super().__init__()
        self.top_level_signals = top_level_signals
        # Connect Top Level Signals
        self.top_level_signals.update_train_model_from_track_model.connect(self.update_train_model_from_track_model)
        self.train_dict = {}  # this will hold trains and delta_x (is essentially our delta_x_dict)
        self.passenger_count = 0

    def update_train_model_from_track_model(self, authority_safe_speed_dict, block_info_dict, add_train,
                                            remove_train, embarking_passengers_update):
        delta_x_dict = {}  # Formatted {Train_ID: delta_x}
        disembarking_passengers_dict = {}  # Formatted {Train_ID: disembarking_passengers}

        # TODO: update delta x from authority_safe_speed_dict and time-lapsed

        # pretty irrelevant: maybe a UI could display block_info_dict

        # if add_train, add a train to dictionary

        # if remove_train != -1, remove train from dictionary at that index

        # pretty irrelevant: update passenger count from embarking_passengers_update
        # pretty irrelevant: generate disembarking passengers when at station

        # End by emitting back to track_model
        self.top_level_signals.update_track_model_from_train_model.emit(delta_x_dict, disembarking_passengers_dict)

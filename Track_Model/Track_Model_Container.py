import os
import sys

from PyQt6.QtWidgets import QApplication

from Track_Model.Track_Model import TrackModel
from Track_Model.Track_Model_UI import Window


class TrackModelContainer(object):
    def __init__(self):
        self.track_model = TrackModel("./Track_Model/Green Line.xlsx")
        self.track_model_ui = Window(self.track_model)

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

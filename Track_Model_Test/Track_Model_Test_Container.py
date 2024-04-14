import sys
import threading

from PyQt6.QtCore import QObject
from PyQt6.QtWidgets import QApplication

from Track_Model.Track_Model_Container import TrackModelContainer
from Track_Model_Test_UI import TrackModelTestLauncherUI


class TrackModelTestContainer(QObject):
    def __init__(self):
        super().__init__()
        self.track_model_container = TrackModelContainer()
        self.track_model_test_container = TrackModelTestLauncherUI()

        # From Wayside to Track Model
        self.track_model_test_container.update_track_model_from_wayside.connect(
            self.track_model_container.update_track_model_from_wayside)
        # From Train Model to Track Model
        self.track_model_test_container.update_track_model_from_train_model.connect(
            self.track_model_container.update_track_model_from_train_model)

    def init_launcher_ui(self):
        app = QApplication.instance()

        if app is None:
            app = QApplication([])  # If QApplication instance doesn't exist, create a new one

        # TODO
        # Create and show the launcher UI
        launcher_ui = TrackModelTestLauncherUI()

        # Create signal connections
        launcher_ui.open_track_model_ui_signal.connect(self.open_track_model_ui)
        launcher_ui.open_test_ui_signal.connect(self.open_test_ui)

        # Show launcher
        launcher_ui.show()

        # run event loop
        app.exec()

    def open_test_ui(self):
        print("Open Time Module UI Signal received")
        self.track_model_test_container.show_ui()

    def open_track_model_ui(self):
        print("Open Track Model UI Signal received")
        self.track_model_container.show_ui()


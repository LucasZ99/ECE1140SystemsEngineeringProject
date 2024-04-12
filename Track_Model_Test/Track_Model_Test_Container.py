import sys
import threading

from PyQt6.QtCore import QObject
from PyQt6.QtWidgets import QApplication

from Track_Model.Track_Model_Container import TrackModelContainer
from Track_Model_Test_UI import TrackModelTestUI, TrackModelTestLauncherUI


class TrackModelTestContainer(QObject):
    def __init__(self):
        super().__init__()
        self.track_model_container = TrackModelContainer()

        self.wayside_test_container = WaysideTestContainer()
        self.train_model_test_container = TrainModelTestContainer()
        # From Wayside to Track Model

        # From Train Model to Track Model
        self.track_controller_container.update_track_model_from_wayside.connect(
            self.track_model_container.update_track_model_from_wayside)

        self.train_model_container.update_track_model_from_train_model.connect(
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
        launcher_ui.open_

        # Show launcher
        launcher_ui.show()

        # run event loop
        app.exec()

    def open_time_module_ui(self):
        print("Open Time Module UI Signal received")
        self.time_module.show_ui()

    def open_ctc_ui(self):
        print("Open CTC UI Signal received")
        self.ctc_container.show_ui()

    def open_track_controller_ui(self, section: str):
        print("Open Track Controller UI Signal received, section:", section)
        self.track_controller_container.show_ui(section)

    def open_track_controller_tb_ui(self):
        print("Open Track Controller TB UI Signal received")
        try:
            self.track_controller_testbench_container.show_ui()
        except Exception as e:
            print(f"Error: {e}")

    def open_track_model_ui(self):
        print("Open Track Model UI Signal received")
        self.track_model_container.show_ui()

    def open_train_controller_SW_ui(self):
        print("Open Train Controller SW UI Signal received")
        self.trainControllerContainer.show_swui()

    def open_train_controller_HW_ui(self):
        print("Open Train Controller HW UI Signal received")
        self.trainControllerContainer.show_hwui()

    def open_train_model_ui(self):
        print("Open Train Model UI Signal received")
        try:
            self.train_model_container.show_ui()
        except Exception as e:
            print(e)


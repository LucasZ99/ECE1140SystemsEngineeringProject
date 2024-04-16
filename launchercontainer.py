import sys
import threading

from PyQt6.QtCore import QObject
from PyQt6.QtWidgets import QApplication

from CTC.CTCContainer import CTCContainer
from SystemTime.SystemTimeContainer import SystemTimeContainer
from TrackControllerTest import TrackControllerTestBenchContainer
from Track_Controller_SW.TrackControllerContainer import TrackControllerContainer
from Track_Model.Track_Model_Container import TrackModelContainer
from launcherui import LauncherUi
from trainControllerTot_Container import TrainController_Tot_Container
from Train_Model import TrainModelContainer


class LauncherContainer(QObject):
    def __init__(self):
        super().__init__()
        self.time_module = SystemTimeContainer()
        self.trainControllerContainer = TrainController_Tot_Container()

        self.train_model_container = TrainModelContainer(self.trainControllerContainer)
        self.track_model_container = TrackModelContainer()
        self.track_controller_container = TrackControllerContainer()
        self.ctc_container = CTCContainer()

        # Test containers
        self.track_controller_testbench_container = TrackControllerTestBenchContainer()

        # Test container signals
        # CTC to Wayside
        self.track_controller_testbench_container.test_update_wayside_from_ctc.connect(self.track_controller_container.update_wayside_from_ctc)
        # Track Model to Wayside
        self.track_controller_testbench_container.test_update_wayside_from_track_model.connect(self.track_controller_container.update_wayside_from_track_model)

        # Connect signals between modules
        # Downstream
        self.ctc_container.update_wayside_from_ctc_signal.connect(
            self.track_controller_container.update_wayside_from_ctc)

        self.track_controller_container.update_track_model_from_wayside.connect(
            self.track_model_container.update_track_model_from_wayside)

        self.track_model_container.update_train_model_from_track_model.connect(
            self.train_model_container.update_train_model_from_track_model)

        # Upstream

        self.train_model_container.update_track_model_from_train_model.connect(
            self.track_model_container.update_track_model_from_train_model)

        self.track_model_container.update_ctc_from_track_model.connect(self.ctc_container.update_ctc_from_track_model)

        self.track_model_container.update_wayside_from_track_model.connect(
            self.track_controller_container.update_wayside_from_track_model)

        self.track_controller_container.update_ctc_from_wayside.connect(self.ctc_container.update_ctc_from_wayside)

        self.launcher_ui = LauncherUi()

    def init_launcher_ui(self):
        # Create signal connections
        self.launcher_ui.open_time_module_ui_signal.connect(self.open_time_module_ui)
        self.launcher_ui.open_track_controller_ui_signal.connect(self.open_track_controller_ui)
        self.launcher_ui.open_track_controller_tb_ui_signal.connect(self.open_track_controller_tb_ui)
        self.launcher_ui.open_track_model_ui_signal.connect(self.open_track_model_ui)
        self.launcher_ui.open_train_controller_SW_ui_signal.connect(self.open_train_controller_SW_ui)
        self.launcher_ui.open_train_controller_HW_ui_signal.connect(self.open_train_controller_HW_ui)
        self.launcher_ui.open_train_model_ui_signal.connect(self.open_train_model_ui)
        self.launcher_ui.open_ctc_ui_signal.connect(self.open_ctc_ui)

        # Show launcher
        self.launcher_ui.show()

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

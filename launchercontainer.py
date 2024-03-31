import sys
import threading

from PyQt6.QtCore import QObject, pyqtSlot
from PyQt6.QtWidgets import QApplication

from SystemTime.SystemTime import SystemTime
from SystemTime.SystemTimeContainer import SystemTimeContainer
from Track_Controller_SW import TrackControllerContainer
from launcherui import LauncherUi
from Train_Model import UITrain


class LauncherContainer(QObject):

    train_model_ui: UITrain

    def __init__(self,
                 time_module: SystemTimeContainer,
                 track_controller_container: TrackControllerContainer):
        super().__init__()
        self.time_module = time_module
        self.track_controller_container = track_controller_container

    def init_launcher_ui(self):
        app = QApplication.instance()

        if app is None:
            app = QApplication([])  # If QApplication instance doesn't exist, create a new one

        # Create and show the launcher UI
        launcher_ui = LauncherUi()

        # Create signal connections
        launcher_ui.open_time_module_ui_signal.connect(self.open_time_module_ui)
        launcher_ui.open_track_controller_ui_signal.connect(self.open_track_controller_ui)
        launcher_ui.open_track_controller_tb_ui_signal.connect(self.open_track_controller_tb_ui)
        launcher_ui.open_train_model_ui_signal.connect(self.open_train_model_ui)

        # Show launcher
        launcher_ui.show()

        # run event loop
        app.exec()

    def open_time_module_ui(self):
        print("Open Time Module UI Signal received")
        self.time_module.show_ui()

    def open_track_controller_ui(self, section: str):
        print("Open Track Controller UI Signal received, section:", section)
        self.track_controller_container.show_ui(section)

    def open_track_controller_tb_ui(self, section: str):
        print("Open Track Controller TB UI Signal received, section:", section)
        self.track_controller_container.show_testbench_ui(section)

    def open_train_model_ui(self):
        print("Open Train Model UI Signal received")
        app = QApplication.instance()

        if app is None:
            app = QApplication([])

        try:
            self.train_model_ui = UITrain()
        except Exception as e:
            print(e)
        self.train_model_ui.show()

        app.exec()

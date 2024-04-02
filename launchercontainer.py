import sys
import threading

from PyQt6.QtCore import QObject, pyqtSlot
from PyQt6.QtWidgets import QApplication

from CTC.CTCContainer import CTCContainer
from SystemTime.SystemTimeContainer import SystemTimeContainer
from Track_Controller_SW.TrackControllerContainer import TrackControllerContainer
from Track_Model.Track_Model_Container import TrackModelContainer
from launcherui import LauncherUi
from Train_Controller_SW.trainControllerSWContainer import Container
from Train_Controller_HW.trainControllerHWContainer import TrainControler_HW_Container
from Train_Model import TrainModelContainer


class LauncherContainer(QObject):
    def __init__(self):
        super().__init__()
        self.time_module = SystemTimeContainer()
        self.track_model_container = TrackModelContainer()
        self.track_controller_container = TrackControllerContainer(track_model=self.track_model_container)
        self.CTC_container = CTCContainer(self.time_module
                                          # self.track_controller_container
                                          )
        self.CTC_container = CTCContainer(self.time_module)
        self.trainControllerSWContainer = Container()
        self.trainControllerHWContainer = TrainControler_HW_Container()
        self.train_model_container = TrainModelContainer()

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
        launcher_ui.open_track_model_ui_signal.connect(self.open_track_model_ui)
        launcher_ui.open_train_controller_SW_ui_signal.connect(self.open_train_controller_sw_ui)
        launcher_ui.open_train_controller_HW_ui_signal.connect(self.open_train_controller_hw_ui)
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

    def open_track_model_ui(self):
        print("Open Track Model UI Signal received")
        self.track_model_container.show_ui()

    def open_train_controller_sw_ui(self):
        print("Open Train Controller SW UI Signal received")
        self.trainControllerSWContainer.show_ui()

    def open_train_controller_hw_ui(self):
        print("Open Train Controller HW UI Signal received")
        self.trainControllerHWContainer.show_ui()

    def open_train_model_ui(self):
        print("Open Train Model UI Signal received")
        try:
            self.train_model_container.show_ui()
        except Exception as e:
            print(e)


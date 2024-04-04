import sys
import threading

from PyQt6.QtCore import QObject, pyqtSlot
from PyQt6.QtWidgets import QApplication

from CTC.CTCContainer import CTCContainer
from SystemTime.SystemTimeContainer import SystemTimeContainer
from Track_Controller_SW.TrackControllerContainer import TrackControllerContainer
from Track_Model.Track_Model_Container import TrackModelContainer
from launcherui import LauncherUi
from trainControllerTot_Container import TrainController_Tot_Container
from Train_Model import TrainModelContainer, TrainBusinessLogic


class LauncherContainer(QObject):
    def __init__(self):
        super().__init__()
        self.time_module = SystemTimeContainer()
        self.trainControllerContainer = TrainController_Tot_Container(self.time_module)
        self.train_model_container = TrainModelContainer(TrainBusinessLogic(), self.trainControllerContainer,
                                                         self.time_module)
        self.track_model_container = TrackModelContainer(train_model_container=self.train_model_container)
        self.track_controller_container = TrackControllerContainer(track_model=self.track_model_container)
        self.ctc_container = CTCContainer(self.time_module, self.track_controller_container)
        self.trainControllerContainer = TrainController_Tot_Container()
        self.train_model_container = TrainModelContainer(TrainBusinessLogic(), self.trainControllerContainer, self.time_module)

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
        launcher_ui.open_train_controller_SW_ui_signal.connect(self.open_train_controller_SW_ui)
        launcher_ui.open_train_controller_HW_ui_signal.connect(self.open_train_controller_HW_ui)
        launcher_ui.open_train_model_ui_signal.connect(self.open_train_model_ui)
        launcher_ui.open_ctc_ui_signal.connect(self.open_ctc_ui)

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

    def open_track_controller_tb_ui(self, section: str):
        print("Open Track Controller TB UI Signal received, section:", section)
        self.track_controller_container.show_testbench_ui(section)

    def open_track_model_ui(self):
        print("Open Track Model UI Signal received")
        self.track_model_container.show_ui()

    def open_train_controller_SW_ui(self):
        print("Open Train Controller SW UI Signal received")
        if self.trainControllerContainer.Ware != True:
            self.trainControllerContainer = TrainController_Tot_Container(self.time_module,True)
        self.trainControllerContainer.show_ui()

    def open_train_controller_HW_ui(self):
        print("Open Train Controller HW UI Signal received")
        if self.trainControllerContainer.Ware != False:
            self.trainControllerContainer = TrainController_Tot_Container(self.time_module,False)
        self.trainControllerContainer.show_ui()

    def open_train_model_ui(self):
        print("Open Train Model UI Signal received")
        try:
            self.train_model_container.show_ui()
        except Exception as e:
            print(e)


import threading

from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QObject, pyqtSignal, QThread
import sys
from CTC.CTCContainer import CTCContainer
from CTCTest.CTCTestUI import CTCTestUIContainer, CTCTestUI
from CTCTest.TrackControllerModel import TrackControllerModel
from SystemTime import SystemTimeContainer


class TrainSystem(QThread):
    def __init__(self, ctc_container: CTCContainer, test_container: CTCTestUIContainer) -> None:
        super().__init__()
        self.ctc_container = ctc_container
        self.test_container = test_container

    # main loop
    def run(self):
        while True:
            self.ctc_container.update_wayside_from_ctc()


class CTCTestContainer(QObject):
    open_test_ui = pyqtSignal()
    open_ctc_ui = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.track_controller = TrackControllerModel()
        self.ctc_container = CTCContainer()
        self.ctc_test_ui_container = CTCTestUIContainer(self.track_controller)
        print("ctc container instantiated")
        self.system_time_container = SystemTimeContainer()
        self.train_system_backend = TrainSystem(self.ctc_container, self.ctc_test_ui_container)

    def init_test_container(self):
        self.ctc_container.update_wayside_from_ctc_signal.connect(
             self.ctc_test_ui_container.update_test_container_from_ctc_slot)
        self.ctc_test_ui_container.update_ctc_from_test_container_signal.connect(
             self.ctc_container.update_ctc_from_wayside)

        self.system_time_container.show_ui()
        self.ctc_container.show_ui()
        self.train_system_backend.start()
        self.ctc_test_ui_container.show_ui()


def run_ctc_test_container():
    app = QApplication(sys.argv)
    ctc_test_container = CTCTestContainer()
    ctc_test_container.init_test_container()
    app.exec()


if __name__ == '__main__':
    sys.settrace
    # ctc_test_thread = threading.Thread(target=run_ctc_test_container)
    # ctc_test_thread.start()
    run_ctc_test_container()

import threading

from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QObject, pyqtSignal, QThread
import sys

from CTC import CTC
from CTC.CTCContainer import CTCContainer
from CTCTest.CTCTestSignals import CTCTestSignals
from CTCTest.CTCTestUI import CTCTestUIContainer, CTCTestUI
from CTCTest.TrackControllerModel import TrackControllerModel
from SystemTime import SystemTimeContainer
from TopLevelSignals import TopLevelSignals


class CTCWorker(QThread):
    def __init__(self, ctc: CTC) -> None:
        super().__init__()
        self.ctc = ctc

    # main loop
    def run(self):
        self.exec()


class CTCTestContainer(QObject):
    open_test_ui = pyqtSignal()
    open_ctc_ui = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.ctc_container = CTCContainer()
        self.ctc_test_ui_container = CTCTestUIContainer()
        print("ctc test container instantiated")
        self.system_time_container = SystemTimeContainer()
        # self.train_system_backend = TrainSystem(self.ctc_container, self.ctc_test_ui_container)

    def init_test_container(self):
        self.system_time_container.show_ui()
        self.ctc_container.show_ui()
        self.ctc_test_ui_container.show_ui()
        # self.train_system_backend.start()


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

from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QObject

from CTC.CTCContainer import CTCContainer
from CTC.CTC_UI_Main import CTCMainWindow
from CTCTest.CTCTestUI import CTCTestUI
from CTCTest.TrackControllerModel import TrackControllerModel
from SystemTime import SystemTimeContainer


class CTCTestContainer(QObject):
    def __init__(self):
        super().__init__()
        self.ctc_container = CTCContainer()
        self.track_controller_model = TrackControllerModel()

    def init_test_ui(self):
        app = QApplication.instance()

        if app is None:
            app = QApplication([])

        test_ui = CTCTestUI(self.track_controller_model)
        test_ui.show()
        self.ctc_container.show_ui()


def run_ctc_test_container():
    app = QApplication([])
    ctc_test_container = CTCTestContainer()
    ctc_test_container.init_test_ui()


if __name__ == '__main__':
    run_ctc_test_container()

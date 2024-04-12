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
        self.system_time_container = SystemTimeContainer()

        app = QApplication.instance()

        if app is None:
            app = QApplication([])

        self.test_ui = CTCTestUI(self.track_controller_model)

        self.ctc_container.show_ui()
        self.system_time_container.show_ui()

        app.exec()

    # def init_test_ui(self):
    #
    #
    #     #  app.exec()
    #
    #
    #     self.ctc_container.show_ui()
    #     self.system_time_container.show_ui()


def run_ctc_test_container():
    app = QApplication([])
    ctc_test_container = CTCTestContainer()
    # ctc_test_container.init_test_ui()
    app.exec()


if __name__ == '__main__':
    run_ctc_test_container()

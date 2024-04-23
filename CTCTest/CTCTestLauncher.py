import sys

from PyQt6.QtCore import QObject, QThread
from PyQt6.QtWidgets import QApplication

from CTC.CTCContainer import CTCContainer
from CTC.CTC_UI_Main import CTCMainWindow
from CTCTest.CTCTestUI import CTCTestUI, CTCTestUIContainer
from SystemTime import SystemTimeUi, SystemTimeContainer


class CTCTestLauncher(QObject):
    def __init__(self):
        super().__init__()
        self.ctc_ui = CTCMainWindow()
        self.test_ui = CTCTestUI()
        self.system_time_ui = SystemTimeUi()

    def open_ctc_ui(self):
        self.ctc_ui.show()

    def open_test_ui(self):
        self.test_ui.show()

    def open_time_ui(self):
        self.system_time_ui.show()

    def open_uis(self):
        self.open_ctc_ui()
        self.open_test_ui()
        self.open_time_ui()


def run_ctc_test_container():
    app = QApplication(sys.argv)

    ui_container = CTCTestLauncher()

    ctc_thread = QThread()
    ctc_container = CTCContainer()
    ctc_container.moveToThread(ctc_thread)

    test_backend_thread = QThread()
    test_backend_container = CTCTestUIContainer()
    test_backend_container.moveToThread(test_backend_thread)

    system_time_thread = QThread()
    system_time_container = SystemTimeContainer()
    system_time_container.moveToThread(system_time_thread)

    ctc_thread.start()
    test_backend_thread.start()
    system_time_thread.start()

    ui_container.open_uis()

    sys.exit(app.exec())


if __name__ == '__main__':
    run_ctc_test_container()

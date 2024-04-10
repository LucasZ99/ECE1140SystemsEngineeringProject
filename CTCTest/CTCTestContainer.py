from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QObject

from CTC.CTCContainer import CTCContainer
from CTC.CTC_UI_Main import CTCMainWindow
from CTCTest.CTCTestUI import CTCTestUI
from SystemTime import SystemTimeContainer


class CTCTestContainer(QObject):
    def __init__(self):
        super().__init__()
        self.system_time = SystemTimeContainer()
        self.ctc_container = CTCContainer(self.system_time)

    def init_test_ui(self):
        ctc_test_app = QApplication([])

        self.ctc_container.show_ui()
        ctc_test_ui = CTCTestUI()
        ctc_test_ui.show()
        ctc_test_ui.show()
        ctc_test_app.exec()


if __name__ == '__main__':
    ctc_test_container = CTCTestContainer()
    ctc_test_container.init_test_ui()

from PyQt6.QtCore import pyqtSignal, pyqtSlot
from PyQt6.QtWidgets import QMainWindow, QWidget


class CTCTestUI(QMainWindow):
    update_ctc_from_track_model = pyqtSignal()
    update_ctc_from_wayside = pyqtSignal(dict, list, list, list)

    def __init__(self):
        super(CTCTestUI, self).__init__()

        self.setWindowTitle('CTC Test UI')

        # Block List
        self.ctc_test_ui_main_layout_widget = QWidget()
        self.setCentralWidget(self.ctc_test_ui_main_layout_widget)

    @pyqtSlot(list, bool, list, list)
    def update_test_ui_from_wayside(self):
        pass


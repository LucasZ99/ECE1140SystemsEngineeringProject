import sys

from PyQt6.QtCore import pyqtSignal, pyqtSlot, QObject
from PyQt6.QtWidgets import QMainWindow, QWidget, QApplication

from CTCTest.TrackControllerModel import TrackControllerModel

from Common.GreenLine import *
from Common import TrackSignal, Light, RRCrossing, Switch


class CTCTestUI(QMainWindow):
    update_ctc_from_track_model = pyqtSignal()
    update_ctc_from_wayside = pyqtSignal(dict, list, list, list)

    def __init__(self, track_controller_model: TrackControllerModel):
        super(CTCTestUI, self).__init__()

        self.setWindowTitle('CTC Test UI')

        self.track_controller_model = track_controller_model

        # Block List
        self.ctc_test_ui_main_layout_widget = QWidget()
        self.setCentralWidget(self.ctc_test_ui_main_layout_widget)


    def show_ctc_test_ui(self):
        app = QApplication(sys.argv)
        # ui = CTCTestUI()
        self.show()
        app.exec()

    @pyqtSlot(list, bool, list, list)
    def update_test_ui_from_wayside(self):
        pass

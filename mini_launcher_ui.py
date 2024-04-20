import sys

from PyQt6.QtCore import QThread
from PyQt6.QtWidgets import QPushButton, QMainWindow, QApplication
from PyQt6.uic import loadUi

from TopLevelSignals import TopLevelSignals
from TrackControllerTest import TrackControllerTestBenchContainer, TrackControllerTestSignals
from TrackControllerTest.TestUi import TestUi
from Track_Controller_SW import TrackControllerSignals
from Track_Controller_SW.TrackControllerContainer import TrackControllerContainer
from Track_Controller_SW.TrackControllerUI import UI


class Ui_MainWindow(QMainWindow):
    def __init__(self, track_controller_test_signals: TrackControllerTestSignals, track_controller_signals: TrackControllerSignals):
        super().__init__()
        loadUi('mini_launcher.ui', self)
        self.test_ui = TestUi(track_controller_test_signals)
        self.track_controller_a_ui = UI("A", track_controller_signals)
        self.track_controller_c_ui = UI("C", track_controller_signals)

        self.track_controller_test_button = self.findChild(QPushButton, "track_controller_test_button")
        self.track_controller_a_button = self.findChild(QPushButton, "track_controller_a_button")
        self.track_controller_c_button = self.findChild(QPushButton, "track_controller_c_button")

        self.track_controller_test_button.clicked.connect(self.open_test_ui)
        self.track_controller_a_button.clicked.connect(self.open_track_controller_a_ui)
        self.track_controller_c_button.clicked.connect(self.open_track_controller_c_ui)

        self.show()

    def open_test_ui(self):
        self.test_ui.show()

    def open_track_controller_a_ui(self):
        self.track_controller_a_ui.show()

    def open_track_controller_c_ui(self):
        self.track_controller_c_ui.show()


def main():

    app = QApplication(sys.argv)

    top_level_signals = TopLevelSignals()
    track_controller_signals = TrackControllerSignals()
    track_controller_test_signals = TrackControllerTestSignals()

    test_thread = QThread()
    test_container = TrackControllerTestBenchContainer(top_level_signals=top_level_signals,
                                                       signals=track_controller_test_signals)
    test_container.moveToThread(test_thread)


    track_controller_thread = QThread()
    track_controller_container = TrackControllerContainer(top_level_signals=top_level_signals,
                                                          signals=track_controller_signals)
    track_controller_container.moveToThread(track_controller_thread)

    test_thread.start()
    track_controller_thread.start()

    window = Ui_MainWindow(track_controller_test_signals=track_controller_test_signals,
                           track_controller_signals=track_controller_signals)

    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()


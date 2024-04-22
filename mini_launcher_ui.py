import sys

from PyQt6.QtCore import QThread
from PyQt6.QtWidgets import QPushButton, QMainWindow, QApplication
from PyQt6.uic import loadUi

from TrackControllerTest import TrackControllerTestBenchContainer
from TrackControllerTest.TestUi import TestUi
from Track_Controller_SW.TrackControllerContainer import TrackControllerContainer
from Track_Controller_SW.TrackControllerUI import UI
from Track_Model.Track_Model_Container import TrackModelContainer
from Track_Model.Track_Model_UI import Window


class Ui_MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        loadUi('mini_launcher.ui', self)
        self.test_ui = TestUi()
        self.track_controller_a_ui = UI("A")
        self.track_controller_c_ui = UI("C")
        self.track_model_ui = Window()
        # self.ctc_ui = CTCUi()
        # self.track_model_ui = TrackModelUI()

        self.track_controller_test_button = self.findChild(QPushButton, "track_controller_test_button")
        self.track_controller_a_button = self.findChild(QPushButton, "track_controller_a_button")
        self.track_controller_c_button = self.findChild(QPushButton, "track_controller_c_button")
        self.ctc_button = self.findChild(QPushButton, "ctc_button")
        self.track_model_button = self.findChild(QPushButton, "track_model_button")

        self.track_controller_test_button.clicked.connect(self.open_test_ui)
        self.track_controller_a_button.clicked.connect(self.open_track_controller_a_ui)
        self.track_controller_c_button.clicked.connect(self.open_track_controller_c_ui)
        self.ctc_button.clicked.connect(self.open_ctc_ui)
        self.track_model_button.clicked.connect(self.open_track_model)

        self.show()

    def open_ctc_ui(self):
        # self.ctc_ui.show()
        pass

    def open_test_ui(self):
        self.test_ui.show()

    def open_track_controller_a_ui(self):
        self.track_controller_a_ui.show()

    def open_track_controller_c_ui(self):
        self.track_controller_c_ui.show()

    def open_track_model(self):
        self.track_model_ui.show()


def main():

    app = QApplication(sys.argv)

    # ctc_signals = CTCSignals()

    # ctc_thread = QThread()
    # ctc_container = CTCContainer(top_level_signals=top_level_signals,
    #                              signals=ctc_signals)
    # ctc_container.moveToThread(ctc_thread)


    test_thread = QThread()
    test_container = TrackControllerTestBenchContainer()
    test_container.moveToThread(test_thread)

    track_controller_thread = QThread()
    track_controller_container = TrackControllerContainer()
    track_controller_container.moveToThread(track_controller_thread)

    track_model_thread = QThread()
    track_model_container = TrackModelContainer()
    track_model_container.moveToThread(track_model_thread)

    # ctc_thread.start()
    test_thread.start()
    track_controller_thread.start()
    # track_model_thread.start()

    window = Ui_MainWindow()

    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()


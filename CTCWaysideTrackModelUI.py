import os
import sys

from PyQt6.QtCore import QThread
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QPushButton, QMainWindow, QApplication, QLabel
from PyQt6.uic import loadUi

from CTC.CTCContainer import CTCContainer
from CTC.CTC_UI_Main import CTCMainWindow
from TrackControllerTest import TrackControllerTestBenchContainer
from TrackControllerTest.TestUi import TestUi
from Track_Controller_SW.TrackControllerContainer import TrackControllerContainer
from Track_Controller_SW.TrackControllerUI import UI
from Track_Model.Track_Model_Container import TrackModelContainer
from Track_Model.Track_Model_UI import Window
from Train_Model import UITrain, TrainModelContainer
from SystemTime import SystemTimeUi, SystemTimeContainer
from Train_Model_Dummy.TrainModelDummyContainer import TrainModelDummyContainer


class UiMainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        current_dir = os.path.dirname(__file__)  # setting up to work in any dir
        ui_path = os.path.join(current_dir, 'CTC_Wayside_TrackModel.ui')
        loadUi(ui_path, self)

        # STYLE
        dirname = os.path.dirname(__file__)
        style_file = os.path.join(dirname, 'Track_Model/style.css')
        with open(style_file, 'r') as file:
            self.setStyleSheet(file.read())
        # FONT
        title_font = QFont()
        title_font.setBold(True)
        title_font.setPointSize(20)
        self.title = QLabel('CTC-Wayside-TrackModel TB')  # TODO: idk how designer works
        self.title.setFont(title_font)

        self.system_time_ui = SystemTimeUi()
        self.track_controller_a_ui = UI("A")
        self.track_controller_c_ui = UI("C")
        self.track_controller_test_ui = TestUi()
        self.track_model_ui = Window()
        self.ctc_ui = CTCMainWindow()

        self.track_controller_a_button = self.findChild(QPushButton, "track_controller_a_button")
        self.track_controller_c_button = self.findChild(QPushButton, "track_controller_c_button")
        self.ctc_button = self.findChild(QPushButton, "ctc_button")
        self.track_model_button = self.findChild(QPushButton, "track_model_button")
        self.time_button = self.findChild(QPushButton, "time_button")

        self.time_button.clicked.connect(self.open_time_ui)
        self.track_controller_a_button.clicked.connect(self.open_track_controller_a_ui)
        self.track_controller_c_button.clicked.connect(self.open_track_controller_c_ui)
        self.ctc_button.clicked.connect(self.open_ctc_ui)
        self.track_model_button.clicked.connect(self.open_track_model)

        self.show()

    def open_time_ui(self):
        self.system_time_ui.show()

    def open_ctc_ui(self):
        # self.ctc_ui.show()
        self.ctc_ui.show()

    def open_track_controller_a_ui(self):
        self.track_controller_a_ui.show()

    def open_track_controller_c_ui(self):
        self.track_controller_c_ui.show()

    def open_track_model(self):
        self.track_model_ui.show()


def main():

    app = QApplication(sys.argv)

    ctc_thread = QThread()
    ctc_container = CTCContainer()
    ctc_container.moveToThread(ctc_thread)

    system_time_thread = QThread()
    system_time_container = SystemTimeContainer()
    system_time_container.moveToThread(system_time_thread)

    track_controller_test_thread = QThread()
    track_controller_test_container = TrackControllerTestBenchContainer()
    track_controller_test_container.moveToThread(track_controller_test_thread)

    track_controller_thread = QThread()
    track_controller_container = TrackControllerContainer()
    track_controller_container.moveToThread(track_controller_thread)

    track_model_thread = QThread()
    track_model_container = TrackModelContainer()
    track_model_container.moveToThread(track_model_thread)

    dummy_train_thread = QThread()
    dummy_train_container = TrainModelDummyContainer()
    dummy_train_container.moveToThread(dummy_train_thread)

    system_time_thread.start()
    ctc_thread.start()
    track_controller_thread.start()
    track_model_thread.start()
    dummy_train_thread.start()
    track_controller_test_thread.start()

    window = UiMainWindow()

    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()

import sys

from PyQt6.QtWidgets import QPushButton, QMainWindow, QApplication
from PyQt6.uic import loadUi
from TrackControllerTest.TestUi import TestUi
from Track_Controller_SW.TrackControllerUI import UI


class Ui_MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi('mini_launcher.ui', self)
        self.test_ui = TestUi()
        self.track_controller_a_ui = UI("A")
        self.track_controller_c_ui = UI("C")

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
    window = Ui_MainWindow()
    window.show()
    app.exec()


if __name__ == "__main__":
    main()


import os
import sys

from PyQt6.QtCore import Qt, pyqtSlot, pyqtSignal
from PyQt6.QtWidgets import QMainWindow, QLCDNumber, QLineEdit, QLabel, QApplication, QPushButton
from PyQt6.uic import loadUi


class SystemTimeUi(QMainWindow):
    multiplier_value_updated_signal = pyqtSignal(float)
    toggle_play_pause_signal = pyqtSignal(bool)

    def __init__(self):
        super().__init__()
        self.setWindowTitle('SystemTime')

        current_dir = os.path.dirname(__file__)  # setting up to work in any dir
        ui_path = os.path.join(current_dir, 'timeUi.ui')
        try:
            loadUi(ui_path, self)
        except Exception as e:
            print("Error with loading UI file: ", e)

        self.pause_play_button = self.findChild(QPushButton, 'pause_play_button')
        self.one_times_button = self.findChild(QPushButton, 'one_times_button')
        self.five_times_button = self.findChild(QPushButton, 'five_times_button')
        self.ten_times_button = self.findChild(QPushButton, 'ten_times_button')
        self.twenty_five_times_button = self.findChild(QPushButton, 'twenty_five_times_button')
        self.fifty_times_button = self.findChild(QPushButton, 'fifty_times_button')
        self.multiplier_label = self.findChild(QLabel, 'multiplier_label')

        self.one_times_button.clicked.connect(self.update_multiplier_one)
        self.five_times_button.clicked.connect(self.update_multiplier_five)
        self.ten_times_button.clicked.connect(self.update_multiplier_ten)
        self.twenty_five_times_button.clicked.connect(self.update_multiplier_twenty_five)
        self.fifty_times_button.clicked.connect(self.update_multiplier_fifty)
        self.pause_play_button.clicked.connect(self.toggle_play_pause_button)

        # self.show()

    def toggle_play_pause_button(self):
        if self.pause_play_button.text() == 'pause':
            self.pause_play_button.setText('play')
            self.toggle_play_pause_signal.emit(False)

        else:
            self.pause_play_button.setText('pause')
            self.toggle_play_pause_signal.emit(True)

    def update_multiplier_one(self):
        self.multiplier_value_updated_signal.emit(1)
        self.multiplier_label.setText(f"Multiplier: 1x")

    def update_multiplier_five(self):
        self.multiplier_value_updated_signal.emit(5)
        self.multiplier_label.setText(f"Multiplier: 5x")

    def update_multiplier_ten(self):
        self.multiplier_value_updated_signal.emit(10)
        self.multiplier_label.setText(f"Multiplier: 10x")

    def update_multiplier_twenty_five(self):
        self.multiplier_value_updated_signal.emit(25)
        self.multiplier_label.setText(f"Multiplier: 25x")

    def update_multiplier_fifty(self):
        self.multiplier_value_updated_signal.emit(50)
        self.multiplier_label.setText(f"Multiplier: 50x")




if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = SystemTimeUi()
    window.show()
    sys.exit(app.exec())

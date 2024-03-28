import os
import sys

from PyQt6.QtCore import Qt, pyqtSlot, pyqtSignal
from PyQt6.QtWidgets import QMainWindow, QLCDNumber, QLineEdit, QLabel, QApplication
from PyQt6.uic import loadUi


class SystemTimeUi(QMainWindow):
    multiplier_value_updated_signal = pyqtSignal(float)
    def __init__(self):
        super().__init__()
        self.setWindowTitle('SystemTime')

        current_dir = os.path.dirname(__file__)  # setting up to work in any dir
        ui_path = os.path.join(current_dir, 'timeUi.ui')
        try:
            loadUi(ui_path, self)
        except Exception as e:
            print("Error with loading UI file: ", e)

        self.time_display = self.findChild(QLCDNumber, 'time_display')
        self.multiplier_value = self.findChild(QLineEdit, 'multiplier_value')
        self.multiplier_label = self.findChild(QLabel, 'multiplier_label')

        self.multiplier_value.editingFinished.connect(self.update_multiplier)

        self.show()

    def update_display(self, current_time: float):
        self.time_display.display(current_time)
        self.show()

    def update_multiplier(self):
        time_str = self.multiplier_value.text()
        if time_str.isnumeric() or time_str.replace(".", "").isnumeric():  # text must be an int or float

            value = float(time_str)
            if value > 10:
                return

            self.multiplier_value_updated_signal.emit(value)

        self.multiplier_label.setText(f"Multiplier: {value}x")





if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = SystemTimeUi()
    window.show()
    sys.exit(app.exec())

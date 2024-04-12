from PyQt6.QtCore import QObject, pyqtSlot
from PyQt6.QtWidgets import QApplication

import SystemTime
from SystemTime.SystemTimeUi import SystemTimeUi


class SystemTimeContainer(QObject):
    def __init__(self):
        super().__init__()

    def show_ui(self):
        app = QApplication.instance()  # Get the QApplication instance

        # app_flag = False
        if app is None:
            app = QApplication([])  # If QApplication instance doesn't exist, create a new one
            # app_flag = True

        print("before ui call")
        self.ui = SystemTimeUi()

        self.ui.multiplier_value_updated_signal.connect(self.multiplier_value_updated)
        self.ui.toggle_play_pause_signal.connect(self.toggle_play_pause)
        print("before ui show")
        self.ui.show()
        print("After ui show")

        # if app_flag is True:
        app.exec()

    @pyqtSlot(bool)
    def toggle_play_pause(self, play_pause_bool: bool):
        if play_pause_bool is True:
            SystemTime.play()
        else:
            SystemTime.pause()

    @pyqtSlot(float)
    def multiplier_value_updated(self, multiplier: float):
        SystemTime.set_multiplier(multiplier)
        print(f"multiplier: {multiplier}")

    def time(self):
        return SystemTime.time()



from PyQt6.QtCore import QObject, pyqtSlot
from PyQt6.QtWidgets import QApplication

import SystemTime
from SystemTime.SystemTimeSignals import SystemTimeSignals


class SystemTimeContainer(QObject):
    def __init__(self):
        super().__init__()
        self.signals = SystemTimeSignals
        self.signals.multiplier_value_updated_signal.connect(self.multiplier_value_updated)
        self.signals.toggle_play_pause_signal.connect(self.toggle_play_pause)

    # def show_ui(self):
    #     print("SystemTimeContainer: show_ui")
    #     # app = QApplication.instance()  # Get the QApplication instance
    #
    #     # app_flag = False
    #     # if app is None:
    #     #     app = QApplication([])  # If QApplication instance doesn't exist, create a new one
    #     #     # app_flag = True
    #
    #     print("SystemTimeContainer: before ui call")
    #
    #     self.signals.multiplier_value_updated_signal.connect(self.multiplier_value_updated)
    #     self.signals.toggle_play_pause_signal.connect(self.toggle_play_pause)
    #     print("SystemTimeContainer: before ui show")
    #     self.ui.show()
    #     print("SystemTimeContainer: After ui show")
    #
    #     # if app_flag is True:
    #     # app.exec()

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



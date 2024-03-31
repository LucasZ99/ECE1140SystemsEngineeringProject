from PyQt6.QtCore import QObject
from PyQt6.QtWidgets import QApplication

from SystemTime.SystemTime import SystemTime
from SystemTime.SystemTimeUi import SystemTimeUi


class SystemTimeContainer(QObject):
    def __init__(self):
        super().__init__()
        self.system_time = SystemTime()

    def show_ui(self):
        app = QApplication.instance()  # Get the QApplication instance

        # app_flag = False
        if app is None:
            app = QApplication([])  # If QApplication instance doesn't exist, create a new one
            # app_flag = True

        print("before ui call")
        self.ui = SystemTimeUi()

        self.ui.multiplier_value_updated_signal.connect(self.multiplier_value_updated)
        print("before ui show")
        self.ui.show()
        print("After ui show")

        # if app_flag is True:
        app.exec()

    def multiplier_value_updated(self, multiplier: float):
        self.system_time.set_multiplier(multiplier)
        print(f"multiplier: {multiplier}")

    def time(self):
        return self.system_time.time()



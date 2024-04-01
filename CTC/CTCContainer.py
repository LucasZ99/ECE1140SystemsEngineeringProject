from PyQt6.QtWidgets import QApplication
from CTC import CTC
from CTC.CTC_UI_Main import CTCMainWindow
from SystemTime import SystemTimeContainer


class CTCContainer:
    def __init__(self, system_time_container: SystemTimeContainer):
        self.system_time = system_time_container.system_time
        self.ctc = CTC(self.system_time)

    def show_ui(self):
        app = QApplication.instance()  # Get the QApplication instance

        # app_flag = False
        if app is None:
            app = QApplication([])  # If QApplication instance doesn't exist, create a new one
            # app_flag = True

        print("before ui call")
        self.ui = CTCMainWindow(self.ctc, self.system_time)
        print("before ui show")
        self.ui.show()
        print("After ui show")

        # if app_flag is True:
        app.exec()


if __name__ == "__main__":
    system_time = SystemTime()
    CTCContainer(CTC(system_time), system_time).show_ui()

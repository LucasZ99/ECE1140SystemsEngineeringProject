from PyQt6.QtCore import QObject, pyqtSlot, pyqtSignal
from PyQt6.QtWidgets import QApplication
from CTC import CTC, GREEN_LINE, TRACK
from CTC.CTC_UI_Main import CTCMainWindow
from SystemTime import SystemTimeContainer
from Track_Controller_SW import TrackControllerContainer, Switch


class CTCContainer(QObject):
    update_ctc_from_wayside_signal = pyqtSignal()

    def __init__(self, system_time_container: SystemTimeContainer):
        super().__init__()
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

    @pyqtSlot(list[tuple[int, int, float]], bool, list[tuple[int, bool]], list)
    def update_wayside_from_ctc(self, authority_speed_update: list[tuple[int, int, float]],
                                maintenance_mode_override_flag: bool,
                                blocks_to_close_open: list[tuple[int, bool]],
                                updated_switches: list[Switch]):
        self.update_ctc_from_wayside_signal.emit(authority_speed_update,
                                                 maintenance_mode_override_flag,
                                                 blocks_to_close_open,
                                                 updated_switches)

    @pyqtSlot(list[tuple[int, int]])
    def update_ctc_from_wayside(self):
        pass

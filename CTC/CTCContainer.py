from PyQt6.QtCore import QObject
from PyQt6.QtWidgets import QApplication
from CTC import CTC
from CTC.CTC_UI_Main import CTCMainWindow
from SystemTime import SystemTimeContainer
from Track_Controller_SW import TrackControllerContainer


class CTCContainer(QObject):
    def __init__(self, system_time_container: SystemTimeContainer, track_controller_container_ref: TrackControllerContainer):
        # self.track_controller_container = track_controller_container
        super().__init__()
        self.track_controller_container_ref = track_controller_container_ref
        self.system_time = system_time_container.system_time
        self.ctc = CTC(self.system_time)

        # self.track_controller_container.occupancy_updated_green_signal.connect(self.update_occupancy)

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

        # @pyqtSlot(list)
        # def update_occupancy(self, occupancy_list):
        # TODO: change update_block_occupancy to take a list instead of blocks:
        #     self.ctc.update_block_occupancy(line_id=0, occupancy_list=occupancy_list)


if __name__ == "__main__":
    system_time = SystemTime()
    CTCContainer(CTC(system_time), system_time).show_ui()

from PyQt6.QtCore import QObject, pyqtSlot
from PyQt6.QtWidgets import QApplication
from CTC import CTC, GREEN_LINE, TRACK
from CTC.CTC_UI_Main import CTCMainWindow
from SystemTime import SystemTimeContainer
from Track_Controller_SW import TrackControllerContainer


class CTCContainer(QObject):
    def __init__(self, system_time_container: SystemTimeContainer, track_controller_container_ref: TrackControllerContainer):

        super().__init__()
        self.track_controller_container_ref = track_controller_container_ref
        self.system_time = system_time_container.system_time
        self.ctc = CTC(self.system_time, self.track_controller_container_ref)

        self.track_controller_container_ref.occupancy_updated_signal.connect(self.update_occupancy)
        self.track_controller_container_ref.switch_toggled_signal.connect(self.update_switch_state)
        self.track_controller_container_ref.lights_updated_signal.connect(self.update_lights)
        self.track_controller_container_ref.rr_crossing_toggled_signal.connect(self.update_rr_crossings)


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

    @pyqtSlot(list)
    def update_occupancy(self, occupancy_list: list):
        for idx, block_status in enumerate(occupancy_list):
            if idx + 1 in TRACK[GREEN_LINE]:
                self.ctc.update_block_occupancy(GREEN_LINE, idx + 1, block_status)

    @pyqtSlot(int)
    def update_switch_state(self, switch: int):
        pass

    @pyqtSlot(int)
    def update_lights(self, light: int):
        pass

    @pyqtSlot(int)
    def update_rr_crossings(self, rr_crossing: int):
        pass

        # TODO: change update_block_occupancy to take a list instead of blocks:
        #     self.ctc.update_block_occupancy(line_id=0, occupancy_list=occupancy_list)


# if __name__ == "__main__":
#     system_time = SystemTime()
#     CTCContainer(CTC(system_time), system_time).show_ui()

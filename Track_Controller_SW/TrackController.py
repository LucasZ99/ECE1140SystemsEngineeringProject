from PyQt6.QtCore import pyqtSignal, QObject, pyqtSlot

from Common import Light, RRCrossing, Switch
from Track_Controller_SW.BusinessLogic import BusinessLogic
from Track_Controller_SW.PLC_Logic import PlcProgram
from Track_Controller_SW.TrackControllerSignals import TrackControllerSignals as signals


class TrackController(QObject):

    def __init__(self, occupancy_dict: dict[int, bool], section: str):
        super().__init__()

        self.block_indexes = list(occupancy_dict.keys())
        self.signals = signals

        if section == "A":
            self.switches_list = \
                [
                    Switch(13, 12, 1, 12),
                    Switch(28, 29, 150, 29)
                ]
            self.lights_list = \
                [
                    Light(12, True),
                    Light(1, False),
                    Light(29, True),
                    Light(150, False)
                ]
            self.rr_crossing = \
                [
                    RRCrossing(19, False)
                ]
            self.plc_logic = PlcProgram(section)
            # self.ui = UI(section)

        elif section == "C":
            self.switches_list = \
                [
                    Switch(77, 76, 101, 76),
                    Switch(85, 86, 100, 86)
                ]
            self.lights_list = \
                [
                    Light(76, True),
                    Light(101, False),
                    Light(86, True),
                    Light(100, False)
                ]
            self.plc_logic = PlcProgram(section)
            # self.ui = UI(section)

        self.occupancy_dict = occupancy_dict
        self.zero_speed_flag_dict = dict(zip(self.block_indexes, [False]*len(self.block_indexes)))
        self.section = section

        self.business_logic = BusinessLogic(
            self.occupancy_dict,
            self.switches_list,
            self.lights_list,
            self.plc_logic,
            self.block_indexes,
            self.section
        )

        self.signals.send_switch_changed_A_signal.connect(self.send_switch_changed_index_A)
        self.signals.send_switch_changed_C_signal.connect(self.send_switch_changed_index_C)
        self.signals.send_rr_crossing_A_signal.connect(self.rr_crossing_updated)
        self.signals.send_lights_signal.connect(self.lights_list_updated)


    @pyqtSlot(int)
    def send_switch_changed_index_A(self, switch_block: int):
        if self.section == "A":
            self.signals.track_controller_A_switch_changed_signal.emit(switch_block)

    @pyqtSlot(int)
    def send_switch_changed_index_C(self, switch_block: int):
        if self.section == "C":
            self.signals.track_controller_C_switch_changed_signal.emit(switch_block)


    @pyqtSlot(bool)
    def rr_crossing_updated(self, rr_crossing_active: bool):
        self.signals.track_controller_A_rr_crossing_signal.emit(rr_crossing_active)

    @pyqtSlot(list)
    def lights_list_updated(self, lights_list: list):
        self.lights_list = lights_list
        if self.section == "A":
            self.signals.track_controller_A_lights_changed_signal.emit(lights_list)
        elif self.section == "C":
            self.signals.track_controller_C_lights_changed_signal.emit(lights_list)

    def update_occupancy(self, block_occupancy_dict: dict[int, bool]):
        unsafe_close_blocks = None
        unsafe_toggle_switches = None
        if self.section == "A":
            # update the zero_speed flag list
            occupancy_changed_result = self.business_logic.occupancy_changed(block_occupancy_dict)

            zero_speed_blocks_25_to_28 = occupancy_changed_result[0]
            unsafe_close_blocks = occupancy_changed_result[1]
            unsafe_toggle_switches = occupancy_changed_result[2]

            self.zero_speed_flag_dict.update({25: zero_speed_blocks_25_to_28[0],
                                              26: zero_speed_blocks_25_to_28[1],
                                              27: zero_speed_blocks_25_to_28[2],
                                              28: zero_speed_blocks_25_to_28[3]})
        if self.section == "C":
            occupancy_changed_result = self.business_logic.occupancy_changed(block_occupancy_dict)

            zero_speed_blocks_77_to_80 = occupancy_changed_result[0]
            unsafe_close_blocks = occupancy_changed_result[1]
            unsafe_toggle_switches = occupancy_changed_result[2]

            self.zero_speed_flag_dict.update({77: zero_speed_blocks_77_to_80[0],
                                              78: zero_speed_blocks_77_to_80[1],
                                              79: zero_speed_blocks_77_to_80[2],
                                              80: zero_speed_blocks_77_to_80[3]})

        self.occupancy_dict = block_occupancy_dict
        return [self.zero_speed_flag_dict, unsafe_close_blocks, unsafe_toggle_switches]

    # def show_ui(self):
        # app = QApplication.instance()  # Get the QApplication instance

        # app_flag = False
        # if app is None:
        #     app = QApplication([])  # If QApplication instance doesn't exist, create a new one
        #     # app_flag = True

        # self.ui.show()

        # if app_flag is True:
        # app.exec()


def main():
    track_controller = TrackController([False] * 36, "A")
    track_controller.show_ui()


if __name__ == "__main__":
    main()

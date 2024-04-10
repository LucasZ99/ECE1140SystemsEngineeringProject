from PyQt6.QtCore import QObject, pyqtSignal
from PyQt6.QtCore import pyqtSlot

from Common import Light, Switch
from Track_Controller_SW.PLC_Logic import PlcProgram


class BusinessLogic(QObject):
    # Define Signals
    occupancy_signal = pyqtSignal(dict)
    switches_signal = pyqtSignal(list)
    switch_changed_index_signal = pyqtSignal(int)
    rr_crossing_signal = pyqtSignal(bool)
    light_signal = pyqtSignal(int)
    lights_list_signal = pyqtSignal(list)

    def __init__(self, block_occupancy: dict, switches_arr: list[Switch], lights_list: list[Light],
                 plc_logic: PlcProgram, block_indexes: list, section: str):
        super().__init__()
        self.occupancy_dict = block_occupancy
        self.switches_list = switches_arr
        self.filepath = None

        self.lights_list = lights_list
        self.plc_logic = plc_logic
        self.num_blocks = len(block_occupancy)
        self.block_indexes = block_indexes
        self.section = section

    # Must call this method whenever occupancy is updated
    @pyqtSlot(list)
    def occupancy_changed(self, new_occupancy: dict):
        print("Occupancy change detected on Track Controller Section: ", self.section)
        self.occupancy_dict = new_occupancy
        self.occupancy_signal.emit(self.occupancy_dict)

        if self.switches_list[0].current_pos == self.switches_list[0].pos_a:
            switch_1 = True
        else:
            switch_1 = False

        if self.switches_list[1].current_pos == self.switches_list[1].pos_a:
            switch_2 = True
        else:
            switch_2 = False

        # execute the plc program when the occupancy changes
        plc_result = self.plc_logic.execute_plc(
            list(self.occupancy_dict.values())
        )
        switch_1_result = plc_result[0]
        switch_2_result = plc_result[1]
        rr_active_result = plc_result[2]
        zero_speed_flags = plc_result[3]
        unsafe_close_blocks = plc_result[4]
        unsafe_toggle_switches = plc_result[5]

        # post plc execution processing logic
        if switch_1_result != switch_1:
            self.switches_changed(0)
            self.lights_list[0].toggle()
            self.lights_list[1].toggle()
            if self.lights_list[0].val is True:
                self.light_signal.emit(0)
        else:
            self.light_signal.emit(1)

        if switch_2_result != switch_2:
            self.switches_changed(1)
            self.lights_list[2].toggle()
            self.lights_list[3].toggle()
            if self.lights_list[2].val is True:
                self.light_signal.emit(2)
            else:
                self.light_signal.emit(3)

        # rr crossing logic
        if rr_active_result is True:
            self.rr_crossing_signal.emit(True)
        else:
            self.rr_crossing_signal.emit(False)

        self.lights_list_signal.emit(self.lights_list)

        # return the zero speed flag update
        return [zero_speed_flags, unsafe_close_blocks, unsafe_toggle_switches]

    @pyqtSlot(int)
    def switches_changed(self, index: int) -> None:

        print(f"Switch at b{self.switches_list[index].block} changed")
        self.switch_changed_index_signal.emit(self.switches_list[index].block)
        self.switches_list[index].toggle()
        self.switches_signal.emit(self.switches_list)

    def set_plc_filepath(self, plc_filepath: str) -> None:
        self.plc_logic.set_filepath(plc_filepath)
        self.filepath = plc_filepath

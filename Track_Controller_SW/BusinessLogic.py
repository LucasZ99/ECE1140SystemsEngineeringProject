from PyQt6.QtCore import QObject, pyqtSignal
from PyQt6.QtCore import pyqtSlot

from Track_Controller_SW.PLC_Logic import PlcProgram
from Track_Controller_SW.switching import Switch


class BusinessLogic(QObject):
    # Define Signals
    occupancy_signal = pyqtSignal(list)
    switches_signal = pyqtSignal(list)
    switch_changed_index_signal = pyqtSignal(int)
    rr_crossing_signal = pyqtSignal(bool)
    light_signal = pyqtSignal(int)
    lights_list_signal = pyqtSignal(list)

    def __init__(self, block_occupancy: list, switches_arr: list[Switch], lights_list: list,
                 plc_logic: PlcProgram, block_indexes: list, section: str):
        super().__init__()
        self.occupancy_list = block_occupancy
        self.switches_list = switches_arr
        self.zero_speed_flag_list = [False] * len(self.occupancy_list)
        self.filepath = None

        self.lights_list = lights_list
        self.plc_logic = plc_logic
        self.num_blocks = len(block_occupancy)
        self.block_indexes = block_indexes
        self.section = section

    # Must call this method whenever occupancy is updated
    @pyqtSlot(list)
    def occupancy_changed(self, new_occupancy: list):
        print("Occupancy change detected on Track Controller: ", self.section)
        self.occupancy_list = new_occupancy
        self.occupancy_signal.emit(self.occupancy_list)

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
            self.occupancy_list
        )

        # post plc execution processing logic
        try:
            if plc_result[0] != switch_1:
                self.switches_changed(0)
                self.lights_list[0].toggle()
                self.lights_list[1].toggle()
                if self.lights_list[0].val is True:
                    self.light_signal.emit(0)
            else:
                self.light_signal.emit(1)
        except Exception as e:
            print(e)
        if plc_result[1] != switch_2:
            self.switches_changed(1)
            self.lights_list[2].toggle()
            self.lights_list[3].toggle()
            if self.lights_list[2].val is True:
                self.light_signal.emit(2)
            else:
                self.light_signal.emit(3)

        # rr crossing logic
        if plc_result[2] is True:
            self.rr_crossing_signal.emit(True)
        else:
            self.rr_crossing_signal.emit(False)

        self.lights_list_signal.emit(self.lights_list)

        # return the zero speed flag update
        return plc_result[3]

    @pyqtSlot(int)
    def switches_changed(self, index: int) -> None:

        print(f"Switch at b{self.switches_list[index].block} changed")
        self.switch_changed_index_signal.emit(self.switches_list[index].block)
        self.switches_list[index].toggle()
        self.switches_signal.emit(self.switches_list)

    def set_plc_filepath(self, plc_filepath: str) -> None:
        self.plc_logic.set_filepath(plc_filepath)
        self.filepath = plc_filepath

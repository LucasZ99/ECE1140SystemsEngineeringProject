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

    def __init__(self, block_occupancy: list, switches_arr: list[Switch], lights_list: list,
                 plc_logic: PlcProgram, block_indexes: list, section: str):
        super().__init__()
        self.occupancy_list = block_occupancy
        self.switches_list = switches_arr
        self.zero_speed_flag_list = [False] * len(self.occupancy_list)
        self.filepath = None
        # TODO add lights_list to constructor

        self.lights_list = lights_list
        self.plc_logic = plc_logic
        self.num_blocks = len(block_occupancy)
        self.block_indexes = block_indexes
        self.section = section

    # Must call this method whenever occupancy is updated
    @pyqtSlot(list)
    def occupancy_changed(self, new_occupancy: list):
        print("Occupancy changed")
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
            self.occupancy_list,
        )

        # post plc execution processing logic
        if plc_result[0] != switch_1:
            self.switches_changed(0)
        if plc_result[1] != switch_2:
            self.switches_changed(1)

        # rr crossing logic
        if plc_result[2] is True:
            self.rr_crossing_signal.emit(True)
        else:
            self.rr_crossing_signal.emit(False)

        # return the zero speed flag update
        return plc_result[3]

    @pyqtSlot(int)
    def switches_changed(self, index: int) -> None:

        print(f"Switch at b{self.switches_list[index].block} changed")
        self.switch_changed_index_signal.emit(self.switches_list[index].block)
        self.switches_list[index].toggle()
        self.switches_signal.emit(self.switches_list)

    @pyqtSlot(list)
    def sug_speed_updated(self, sug_speed: float) -> None:
        self.suggested_speed_list[0] = sug_speed

        print(f"Suggested speed updated to {self.suggested_speed_list[0]}")

    def set_plc_filepath(self, plc_filepath: str) -> None:
        self.plc_logic.set_filepath(plc_filepath)
        self.filepath = plc_filepath

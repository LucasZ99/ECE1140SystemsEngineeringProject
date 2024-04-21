import sys

from PyQt6.QtCore import QObject, pyqtSignal
from PyQt6.QtCore import pyqtSlot

from Common import Light, Switch
from Track_Controller_SW.PLC_Logic import PlcProgram
from Track_Controller_SW.TrackControllerSignals import TrackControllerSignals as signals


class BusinessLogic(QObject):

    def __init__(self, block_occupancy: dict, switches_arr: list[Switch], lights_list: list[Light],
                 plc_logic: PlcProgram, block_indexes: list, section: str):
        super().__init__()
        self.occupancy_dict = block_occupancy
        self.switches_list = switches_arr
        self.signals = signals

        self.lights_list = lights_list
        self.plc_logic = plc_logic
        self.filepath = self.plc_logic.filepath

        self.num_blocks = len(block_occupancy)
        self.block_indexes = block_indexes
        self.section = section
        self.unsafe_toggle_switches = []

        self.signals.get_switches_list_A_switch_ui_signal.connect(self.send_switches_switch_ui_A)
        self.signals.get_switches_list_C_switch_ui_signal.connect(self.send_switches_switch_ui_C)
        self.signals.get_switches_list_A_signal.connect(self.send_switches_A)
        self.signals.get_switches_list_C_signal.connect(self.send_switches_C)
        self.signals.get_occupancy_A_signal.connect(self.send_occupancy_A)
        self.signals.get_occupancy_C_signal.connect(self.send_occupancy_C)
        self.signals.get_lights_A_signal.connect(self.send_lights_A)
        self.signals.get_lights_C_signal.connect(self.send_lights_C)
        self.signals.get_filename_A_signal.connect(self.send_filename_A)
        self.signals.get_filename_C_signal.connect(self.send_filename_C)

        self.signals.maintenance_switch_changed_A_signal.connect(self.switches_changed_A)
        self.signals.maintenance_switch_changed_C_signal.connect(self.switches_changed_C)

        self.signals.set_plc_filepath_A_signal.connect(self.set_plc_filepath_A)
        self.signals.set_plc_filepath_C_signal.connect(self.set_plc_filepath_C)




    @pyqtSlot()
    def send_switches_switch_ui_A(self):
        if self.section == "A":
            self.signals.send_switches_list_A_switch_ui_signal.emit(self.switches_list)

    @pyqtSlot()
    def send_switches_switch_ui_C(self):
        if self.section == "C":
            self.signals.send_switches_list_C_switch_ui_signal.emit(self.switches_list)

    @pyqtSlot()
    def send_switches_A(self):
        if self.section == 'A':
            self.signals.send_switches_list_A_signal.emit(self.switches_list)

    @pyqtSlot()
    def send_switches_C(self):
        if self.section == 'C':
            self.signals.send_switches_list_C_signal.emit(self.switches_list)

    @pyqtSlot()
    def send_occupancy_A(self):
        if self.section == 'A':
            self.signals.send_occupancy_A_signal.emit(self.occupancy_dict)

    @pyqtSlot()
    def send_occupancy_C(self):
        if self.section == 'C':
            self.signals.send_occupancy_C_signal.emit(self.occupancy_dict)

    @pyqtSlot()
    def send_lights_A(self):
        if self.section == 'A':
            self.signals.init_lights_A_signal.emit(self.lights_list)

    @pyqtSlot()
    def send_lights_C(self):
        if self.section == 'C':
            self.signals.init_lights_C_signal.emit(self.lights_list)

    @pyqtSlot()
    def send_filename_A(self):
        if self.section == 'A':
            self.signals.send_filename_A_signal.emit(self.filepath[-21:])

    @pyqtSlot()
    def send_filename_C(self):
        if self.section == 'C':
            self.signals.send_filename_C_signal.emit(self.filepath[-21:])

    @pyqtSlot(list)
    def occupancy_changed(self, new_occupancy: dict):
        print(f"WAYSIDE_{self.section}: Occupancy change detected on Track Controller Section: ", self.section)

        self.occupancy_dict = new_occupancy

        if self.section == "A":
            self.signals.send_occupancy_A_signal.emit(self.occupancy_dict)
        else:
            self.signals.send_occupancy_C_signal.emit(self.occupancy_dict)

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
        self.unsafe_toggle_switches = plc_result[5]

        # post plc execution processing logic
        if switch_1_result != switch_1:
            if self.section == 'A':
                self.switches_changed_A(0)
            else:
                self.switches_changed_C(0)
            self.lights_list[0].toggle()
            self.lights_list[1].toggle()
            if self.lights_list[0].val is True:
                if self.section == 'A':
                    self.signals.send_light_A_signal.emit(0)
                else:
                    self.signals.send_light_C_signal.emit(0)
            else:
                if self.section == 'A':
                    self.signals.send_light_A_signal.emit(1)
                else:
                    self.signals.send_light_C_signal.emit(1)

        if switch_2_result != switch_2:
            if self.section == 'A':
                self.switches_changed_A(1)
            else:
                self.switches_changed_C(1)
            self.lights_list[2].toggle()
            self.lights_list[3].toggle()
            if self.lights_list[2].val is True:
                if self.section == 'A':
                    self.signals.send_light_A_signal.emit(2)
                else:
                    self.signals.send_light_C_signal.emit(2)
            else:
                if self.section == 'A':
                    self.signals.send_light_A_signal.emit(3)
                else:
                    self.signals.send_light_C_signal.emit(3)

        # rr crossing logic
        if self.section == 'A':
            if rr_active_result is True:
                self.signals.send_rr_crossing_A_signal.emit(True)
            else:
                self.signals.send_rr_crossing_A_signal.emit(False)

        if self.section == 'A':
            self.signals.init_lights_A_signal.emit(self.lights_list)
        else:
            self.signals.init_lights_C_signal.emit(self.lights_list)

        self.signals.send_lights_signal.emit(self.lights_list)

        # return the zero speed flag update
        return [zero_speed_flags, unsafe_close_blocks, self.unsafe_toggle_switches]

    @pyqtSlot(int)
    def switches_changed_A(self, index: int) -> None:
        if self.section == "A":
            if index not in self.unsafe_toggle_switches:
                print(f"WAYSIDE_{self.section}: Switch at b{self.switches_list[index].block} changed")

                self.switches_list[index].toggle()
                self.signals.send_switch_changed_A_signal.emit(self.switches_list[index].block)
                self.signals.send_switches_list_A_signal.emit(self.switches_list)

    @pyqtSlot(int)
    def switches_changed_C(self, index: int) -> None:
        if self.section == "C":
            if index not in self.unsafe_toggle_switches:
                print(f"WAYSIDE_{self.section}: Switch at b{self.switches_list[index].block} changed")

                self.switches_list[index].toggle()
                self.signals.send_switch_changed_C_signal.emit(self.switches_list[index].block)
                self.signals.send_switches_list_C_signal.emit(self.switches_list)

    def set_plc_filepath_A(self, plc_filepath: str) -> None:
        if self.section == "A":
            self.plc_logic.set_filepath(plc_filepath)
            self.filepath = plc_filepath
            print('WAYSIDE: filepath a updated')

    def set_plc_filepath_C(self, plc_filepath: str) -> None:
        if self.section == "C":
            self.plc_logic.set_filepath(plc_filepath)
            self.filepath = plc_filepath
            print('WAYSIDE: filepath c updated')



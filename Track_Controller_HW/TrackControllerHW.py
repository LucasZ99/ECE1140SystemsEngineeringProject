import time
import os
import sys
from PyQt6.QtCore import pyqtSignal, QObject, pyqtSlot
from Track_Controller_HW import SlotsSigs, TBShell


class TrackControllerHardware(QObject):
    mode = False
    num_switches = 1
    num_blocks = 107
    authority = [0] * num_blocks
    switches = [False] * num_switches
    blocks = [False] * num_blocks
    suggested_speed = [0.0] * num_blocks
    stops = [False] * num_blocks
    rr_crossing = False

    rr_crossing_signal = pyqtSignal(bool)

    def __init__(self, occupancy_list: list, section: str):
        super().__init__()
        self.blocks = occupancy_list
        self.slots_sigs = SlotsSigs(mode=self.mode, authority=self.authority, switches=self.switches,
                                              blocks=self.blocks, suggested_speed=self.suggested_speed,
                                              rr_crossing=self.rr_crossing)

        self.tb_shell = TBShell.TB_Shell(self.slots_sigs)
        self.slots_sigs.rr_crossing_signal.connect(self.rr_crossing_updated)

    def update_occupancy(self, block_occupancy_list: list):
        self.blocks = block_occupancy_list
        self.stops = self.slots_sigs.new_occupancy(block_occupancy_list)
        print(self.blocks)
        return self.stops

    def show_testbench_ui(self):
        print("Showing TestBench UI")
        self.tb_shell.show_ui()

    @pyqtSlot(bool)
    def rr_crossing_updated(self, rr_crossing_new_val: bool):
        print("rr cross updated")
        self.rr_crossing = rr_crossing_new_val
        self.rr_crossing_signal.emit(rr_crossing_new_val)


if __name__ == '__main__':
    track_controller_hw = TrackControllerHardware(occupancy_list=[True] * 105, section="B")
    track_controller_hw.show_testbench_ui()
    #track_controller_hw.send_to_hw()
    #print("HW data sent successfully")


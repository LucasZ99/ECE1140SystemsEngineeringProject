import time
import os
import sys
import itertools
from PyQt6.QtCore import pyqtSignal, QObject, pyqtSlot
from Track_Controller_HW import SlotsSigs, TBShell

class TrackControllerHardware(QObject):
    mode = False
    num_switches = 1
    num_blocks = 107
    authority = [0] * num_blocks
    switches = [False] * num_switches
    blocks = {}
    suggested_speed = [0.0] * num_blocks
    stops = {}
    rr_crossing = False

    rr_crossing_signal = pyqtSignal(bool)

    def __init__(self, occupancy_dict: dict, section: str):
        super().__init__()
        self.blocks = occupancy_dict
        self.slots_sigs = SlotsSigs(mode=self.mode, authority=self.authority, switches=self.switches,
                                              blocks=self.blocks, suggested_speed=self.suggested_speed,
                                              rr_crossing=self.rr_crossing)

        self.tb_shell = TBShell.TB_Shell(self.slots_sigs)
        self.slots_sigs.rr_crossing_signal.connect(self.rr_crossing_updated)

    def update_occupancy(self, block_occupancy_dict: dict[int, bool]):
        print("WS HW: track controller B update occupancy called")
        self.blocks = block_occupancy_dict
        self.stops = self.slots_sigs.new_occupancy(block_occupancy_dict)
        print("blck occup list blck B: ", self.blocks)
        print("stops list blck B:      ", self.stops)
        return self.stops

    def show_testbench_ui(self):
        print("Showing TestBench UI")
        self.tb_shell.show_ui()

    @pyqtSlot(bool)
    def rr_crossing_updated(self, rr_crossing_new_val: bool):
        print("WS HW: rr cross updated")
        self.rr_crossing = rr_crossing_new_val
        self.rr_crossing_signal.emit(rr_crossing_new_val)

    def rr_cross_test(self, blocks: dict, expected_rr_cross_val: bool):
        self.blocks = blocks  # set the blocks to the new occupancy
        self.stops = self.slots_sigs.new_occupancy(blocks)  # update the occupancy
        # PLC logic will update the rr_crossing value based on the occupancy
        #print("blck occup list blck B: ", self.blocks)
        #print("stops list blck B:      ", self.stops)
        if self.rr_crossing == expected_rr_cross_val:  # check if the rr_crossing value is as expected
            print("Test Passed")
        elif self.rr_crossing != expected_rr_cross_val:
            print("Test Failed")
        #print(blocks, blocks)
        #print("stops", self.stops)

if __name__ == '__main__':
    occupancy_dict = {}
    for i in range(1, 58):
        occupancy_dict[i] = False
    for i in range(62, 151):
        occupancy_dict[i] = False

    occupancy_dict_B = dict(itertools.islice(occupancy_dict.items(), 28, 72))
    occupancy_dict_B.update(dict(itertools.islice(occupancy_dict.items(), 96, 146)))

    track_controller_hw = TrackControllerHardware(occupancy_dict_B, section="B")  # init with default vals
    track_controller_hw.slots_sigs.mode = True  # set the mode to True (manual mode)

    for i in occupancy_dict_B.keys():
        new_occupancy_list = {key: False for key, value in occupancy_dict_B.items() if isinstance(value, bool)}  # create a new list to update the occupancy
        new_occupancy_list[i] = True  # set the occupancy of block 56 to True (a rr_crossing block)
        track_controller_hw.rr_cross_test(new_occupancy_list, True)  # test the PLC's rr_crossing logic
        if i == 150:
            i = 26
        time.sleep(.5)

import time
import os
import sys
from Track_Controller_HW import TBShell
#from Track_Controller_HW import HardwareUI
from Track_Controller_HW import SlotsSigs
import socket


class TrackControllerHardware(object):
    mode = False
    num_switches = 1
    num_blocks = 15
    authority = [0] * num_blocks
    switches = [False] * num_switches
    blocks = [False] * num_blocks
    suggested_speed = [0.0] * num_blocks
    rr_crossing = [0]
    traffic_lights = [0] * num_switches

    def __init__(self, occupancy_list: list, section: str):
        self.blocks = occupancy_list
        self.slots_sigs = SlotsSigs.SlotsSigs(mode=self.mode, authority=self.authority, switches=self.switches,
                                              blocks=self.blocks, suggested_speed=self.suggested_speed,
                                              rr_crossing=self.rr_crossing, traffic_lights=self.traffic_lights)

        self.tb_shell = TBShell.TB_Shell(self.slots_sigs)


    def show_testbench_ui(self):
        print("Showing TestBench UI")
        self.tb_shell.show_ui()

    def send_to_hw(self):
        print("Sending data to HW")

if __name__ == '__main__':
    track_controller_hw = TrackControllerHardware(occupancy_list=[True] * 105, section="A")
    track_controller_hw.show_testbench_ui()
    #track_controller_hw.send_to_hw()
    #print("HW data sent successfully")


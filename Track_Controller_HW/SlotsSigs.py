from PyQt6.QtCore import QObject, pyqtSignal
from PyQt6.QtCore import pyqtSlot
import os
import sys
from Track_Controller_HW.HardwareUI import HWUI

current_dir = os.path.dirname(__file__)  # setting up dir to work in any location in a directory

class SlotsSigs(QObject):
    plc_path = ''  # updated at import time
    # Define Signals
    occupancy_signal = pyqtSignal(list)
    switches_signal = pyqtSignal(list)
    suggested_speed_signal = pyqtSignal(list)
    rr_crossing_signal = pyqtSignal(bool)

    def __init__(self, mode: bool, authority: list, switches: list, blocks: list,
                 suggested_speed: list, rr_crossing: bool):
        # assigning values to the signals

        self.new_rr_crossing = False
        self.plc_import()  # import PLC
        sys.path.append(self.plc_path)
        import PLCProgram  # will never get to this point unless the PLC file is found
        self.plc = PLCProgram.PLC()

        super().__init__()
        self.mode = mode
        self.authority = authority
        self.switches = switches
        self.blocks = blocks
        self.suggested_speed = suggested_speed
        self.rr_crossing = rr_crossing
        self.hw_ui = HWUI()
        self.stops = [False] * len(self.blocks)

    # Signal to update the occupancy
    @pyqtSlot(list)
    def new_occupancy(self, new_occupancy: list):
        print("new occupancy")
        self.blocks = new_occupancy
        self.plc.assign_vals(self.blocks, self.switches, self.rr_crossing, self.mode)
        self.stops, self.blocks, self.new_rr_crossing = self.plc.run_plc_logic()
        self.occupancy_signal.emit(new_occupancy)
        print("rr_crossing: ", self.rr_crossing)
        print("new_rr_crossing: ", self.new_rr_crossing)
        if self.rr_crossing != self.new_rr_crossing:
            self.rr_crossing_signal.emit(True)
        else:
            self.rr_crossing_signal.emit(False)
        self.rr_crossing = self.new_rr_crossing
        self.hw_ui.show_hw_data(self.blocks, self.mode, self.rr_crossing, self.switches)
    # Signal to update the switches
    @pyqtSlot(list)
    def new_switches(self, new_switches: list):
        print("switch moved")
        self.switches = new_switches
        self.hw_ui.show_hw_data(self.blocks, self.mode, self.rr_crossing, self.switches)
        self.switches_signal.emit(new_switches)

    @pyqtSlot(bool)
    def rr_crossing_toggled_signal(self, new_rr_crossing: bool):
        print("rr cross toggled")
        self.rr_crossing = new_rr_crossing
        self.hw_ui.show_hw_data(self.blocks, self)
        self.rr_crossing_signal.emit(new_rr_crossing)

    # Signal to update the suggested speed
    @pyqtSlot(list)
    def new_speed(self, new_speed: list):
        print("suggested speed changed")
        self.suggested_speed = new_speed
        self.suggested_speed_signal.emit(new_speed)

    def plc_import(self):  # guarded import of PLC, checking for existence in a specified folder of a USB drive
        print("running PLC import wizard...")
        path = os.path.join(os.path.dirname(__file__), 'PLC')
        file = 'PLCProgram.py'

        try:  # guarded import of PLC prog
            if os.path.exists(path):
                fullpath = os.path.join(path, file)  # found a drive!
                if os.path.isfile(fullpath):
                    print("Found the PLC file!")  # found the file! imported
                    self.plc_path = path  # Location of PLCProgram

                else:
                    print("File does not exist on drive or is in the wrong path")
                    print("Correct path is " + path)
                    sys.exit(1)
            else:
                print("No PLC installed... exiting")  # No drive found
                sys.exit(1)
        except Exception as e:
            print("Something went wrong while trying to import", e)
            sys.exit(1)

    def send_to_hw(self):
        print("Sending data to HW")
        self.hw_ui.show_hw_data(self.blocks, self.mode, self.rr_crossing, self.switches)

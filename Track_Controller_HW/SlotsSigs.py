from PyQt6.QtCore import QObject, pyqtSignal
from PyQt6.QtCore import pyqtSlot
import os
import sys

current_dir = os.path.dirname(__file__)  # setting up dir to work in any location in a directory

class SlotsSigs(QObject):
    plc_path = ''  # updated at import time
    # Define Signals
    occupancy_signal = pyqtSignal(list)
    switches_signal = pyqtSignal(list)
    suggested_speed_signal = pyqtSignal(list)
    rr_crossing_signal = pyqtSignal(list)

    def __init__(self, mode: bool, authority: list, switches: list, blocks: list,
                 suggested_speed: list, rr_crossing: list, traffic_lights: list):
        # assigning values to the signals

        #self.plc_import()  # import PLC
        #sys.path.append(self.plc_path)
        #import PLCProgram  # will never get to this point unless the PLC file is found
        #plc = PLCProgram.PLC()

        super().__init__()
        self.mode = mode
        self.authority = authority
        self.switches = switches
        self.blocks = blocks
        self.suggested_speed = suggested_speed
        self.rr_crossing = rr_crossing
        self.traffic_lights = traffic_lights

    # Signal to update the occupancy
    @pyqtSlot(list)
    def new_occupancy(self, new_occupancy: list):
        print("new occupancy")
        self.occupancy_signal.emit(new_occupancy)

    # Signal to update the switches
    @pyqtSlot(list)
    def new_switches(self, new_switches: list):
        print("switch moved")
        self.switches_signal.emit(new_switches)

    # Signal to update the suggested speed
    @pyqtSlot(list)
    def new_speed(self, new_speed: list):
        print("suggested speed changed")
        self.suggested_speed_signal.emit(new_speed)

    def plc_import(self):  # guarded import of PLC, checking for existence in a specified folder of a USB drive
        print("running PLC import wizard...")
        path = 'F:/PLC'
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
                print("No flash drive inserted... exiting")  # No drive found
                sys.exit(1)
        except Exception as e:
            print("Something went wrong while trying to import", e)
            sys.exit(1)
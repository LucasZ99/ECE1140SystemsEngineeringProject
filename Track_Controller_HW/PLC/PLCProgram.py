# This is the PLC Program.
# This is responsible for modifying the switch, rrCross, and traffic light status of the system
# Must be loaded externally and only use boolean variables
# Author: Devin James
# 2/17/2024

# Functions:
# Loaded externally (USB)
# ability to switch the state of a switch, rrCrossing, and toggle traffic lights
# update main when any change is performed

class PLC:  # watchdog behavior for the PLC data
    def assign_vals(self, blocks, switches, rrCrossing, mode):
        self.rrCrossing = rrCrossing  # False = off
        self.switches = []  # False = 'L'
        self.blocks = blocks  # False = unoccupied
        self.stops = [False] * len(blocks)  # False = no stop
        self.mode = False  # False = auto mode,so the PLC can move everything. In False, PLC can only adjust rrCrossing and trafficLts

    def run_plc_logic(self):  # very simple operations done to show changes
        #if blocks[]
        if self.blocks[0]:
            self.rrCrossing = True
        return [self.stops, self.blocks, self.rrCrossing]  # return the updated values
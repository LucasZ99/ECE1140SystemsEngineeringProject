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
    rrCrossing = False
    switches = []
    blocks = {}
    stops = {}
    mode = False

    def assign_vals(self, blocks, switches, rrCrossing, mode):
        self.rrCrossing = rrCrossing  # False = off
        self.switches = []  # False = 'L'
        self.blocks = blocks  # False = unoccupied
        self.mode = False  # False = auto mode,so the PLC can move everything. In False, PLC can only adjust rrCrossing and trafficLts

    def run_plc_logic(self):  # very simple operations done to show changes
        self.stops = [False] * len(self.blocks)  # False = no stop

        # RR Crossing Logic
        if self.blocks[56] or self.blocks[57] or self.blocks[55]:
            self.rrCrossing = True
        else:
            self.rrCrossing = False

        # stops logic
        for i in range(1, 47):  # blocks 1-46
            if self.blocks[i]:
                match i:
                    case 1:
                        self.stops[i] = True
                    case 2:
                        self.stops[i-1] = True
                    case 3:
                        self.stops[i-1] = True
                        self.stops[i-2] = True
                    case 4:
                        self.stops[i-1] = True
                        self.stops[i-2] = True
                        self.stops[i-3] = True
                    case _:
                        if i >= 5:
                            self.stops[i-1] = True
                            self.stops[i-2] = True
                            self.stops[i-3] = True
                            self.stops[i-4] = True

        for i in range(47, 96):  # blocks 46-96
            if self.blocks[i]:
                match i:
                    case 51:
                        self.stops[i] = True
                    case 52:
                        self.stops[i-1] = True
                    case 53:
                        self.stops[i-1] = True
                        self.stops[i-2] = True
                    case 54:
                        self.stops[i-1] = True
                        self.stops[i-2] = True
                        self.stops[i-3] = True
                    case _:
                        if i <= 55:
                            self.stops[i-1] = True
                            self.stops[i-2] = True
                            self.stops[i-3] = True
                            self.stops[i-4] = True

        return [self.stops, self.blocks, self.rrCrossing]  # return the updated values

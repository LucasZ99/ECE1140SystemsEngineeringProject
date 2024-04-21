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
        self.stops = {key: False for key, value in self.blocks.items() if isinstance(value, bool)}

    def run_plc_logic(self):  # very simple operations done to show changes

        # RR Crossing Logic
        if self.blocks[107] or self.blocks[108] or self.blocks[109]:
            self.rrCrossing = True
        else:
            self.rrCrossing = False

        # stops logic (padding any occupancies with 4 zero speed flags)
        for i in range(29, 76):  # blocks 29 - 57
            #print(self.blocks[i])
            if 58 <= i < 62:
                skipped = True
            elif self.blocks.get(i, False):
                self.stops[i] = True
                if i > 29:
                    self.stops[i - 1] = True
                if i > 30:
                    self.stops[i - 2] = True
                if i > 31:
                    self.stops[i - 3] = True
                if i > 32:
                    self.stops[i - 4] = True

        # for i in range(62, 76):
        #     if self.blocks.get(i, False):
        #         self.stops[i] = True
        #         if i > 62:
        #             self.stops[i - 1] = True
        #         if i > 63:
        #             self.stops[i - 2] = True
        #         if i > 64:
        #             self.stops[i - 3] = True
        #         if i > 65:
        #             self.stops[i - 4] = True

        for i in range(101, 150):  # blocks 101 - 150
            if self.blocks.get(i, False):
                self.stops[i] = True
                if i > 101:
                    self.stops[i - 1] = True
                if i > 102:
                    self.stops[i - 2] = True
                if i > 103:
                    self.stops[i - 3] = True
                if i > 104:
                    self.stops[i - 4] = True

        #print("stops:", self.stops)

        return [self.stops, self.blocks, self.rrCrossing]  # return the updated values

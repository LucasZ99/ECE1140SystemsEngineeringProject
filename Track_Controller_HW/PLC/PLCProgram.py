# This is the PLC Program.
# This is responsible for modifying the switch, rrCross, and traffic light status of the system
# Must be loaded externally and only use boolean variables
# Author: Devin James
# 2/17/2024

class PLC:
    rrCrossing = False
    switches = []
    blocks = {}
    stops = {}
    mode = False
    loopOcc = [False, False]  # [0] = loop 1, [1] = loop 2

    def assign_vals(self, blocks, switches, rrCrossing, mode):
        self.rrCrossing = rrCrossing  # False = off
        self.switches = []  # False = 'L'
        self.blocks = blocks  # False = unoccupied
        self.mode = mode  # False = auto mode,so the PLC can move everything. In False, PLC can only adjust rrCrossing and trafficLts
        self.stops = {key: False for key, value in self.blocks.items() if isinstance(value, bool)}

    def run_plc_logic(self):  # very simple operations done to show changes

        # RR Crossing Logic
        if self.blocks[107] or self.blocks[108] or self.blocks[109]:
            self.rrCrossing = True
        else:
            self.rrCrossing = False

        # stops logic (padding any occupancies with 4 zero speed flags)
        for i in range(29, 77):  # blocks 29 - 76
            #print(self.blocks[i])
            if 58 <= i < 62:
                skipped = True
            elif self.blocks.get(i, False):
                #self.stops[i] = True
                if i > 29:
                    self.stops[i - 1] = True
                if i > 30:
                    self.stops[i - 2] = True
                if i > 31:
                    self.stops[i - 3] = True
                if i > 32:
                    self.stops[i - 4] = True

            # checking for loop 1 occupancy
            if self.blocks.get(76, False):
                self.loopOcc[0] = True
                #print("set loop 1 to occupied")

            if self.loopOcc[0] == True and not self.blocks.get(101, True):  # if loop 1 is occupied and block 101 is unoccupied
                #print ("hit event")
                self.stops[76] = True  # stop the train at block 76 - 73
                self.stops[75] = True
                self.stops[74] = True
                self.stops[73] = True

            if self.blocks.get(101, False):
                self.loopOcc[0] = False

        for i in range(101, 151):  # blocks 101 - 150
            if self.blocks.get(i, False):
                #self.stops[i] = True
                if i > 101:
                    self.stops[i - 1] = True
                if i > 102:
                    self.stops[i - 2] = True
                if i > 103:
                    self.stops[i - 3] = True
                if i > 104:
                    self.stops[i - 4] = True

                # checking for loop 2 occupancy
            if self.blocks.get(150, False):
                self.loopOcc[1] = True
                print("set loop 2 to occupied")

            if self.loopOcc[1] == True and not self.blocks.get(29, True):  # if loop 1 is occupied and block 101 is unoccupied
                print("hit event")
                self.stops[150] = True  # stop the train at block 76 - 73
                self.stops[149] = True
                self.stops[148] = True
                self.stops[147] = True

            if self.blocks.get(29, False):
                print("set loop 2 to unoccupied")
                self.loopOcc[1] = False
        #print("stops:", self.stops)

        return [self.stops, self.blocks, self.rrCrossing]  # return the updated values

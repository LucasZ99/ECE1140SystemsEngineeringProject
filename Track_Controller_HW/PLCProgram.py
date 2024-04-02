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
    def __init__(self):
        self.rrCrossing = [False]  # False = off
        self.trafficLights = [False]  # False = off
        self.switches = []  # False = 'L'
        self.blocks = [True, True, True, True]
        self.mode = False  # False = auto mode,so the PLC can move everything. In False, PLC can only adjust rrCrossing and trafficLts

    def assign_plc_data(self, rrCross, traffLights, switch, block, mod):  # updates globals when passed the vals from main
        self.rrCrossing = rrCross
        self.trafficLights = traffLights
        self.switches = switch
        self.blocks = block
        self.mode = mod

    def run_plc_logic(self):  # very simple operations done to show changes
        if self.blocks[1]:
            self.rrCrossing = True
        elif not self.blocks[1] and not self.blocks[2] and not self.blocks[3]:
            self.rrCrossing = False

        if (self.blocks[11] or self.blocks[6]) and not self.mode:
            self.switches[0] = not self.switches[0]
            self.trafficLights[0] = not self.trafficLights[0]

    def plc_to_main(self):  # pushes the current data to main
        return self.rrCrossing, self.trafficLights, self.switches

    #print("I am the mystical magical PLC creature")

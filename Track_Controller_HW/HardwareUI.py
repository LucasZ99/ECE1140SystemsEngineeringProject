# This is the Hardware UI.
# This receives data from the Main Module, for the purpose of display
# also has a switch to enable maintenance mode, which will allow the manual flipping of switches
# Author: Devin James
# 2/17/2024

# Functions:
# map arduino pins to outputs for displaying current system status (switches, block occupancy, traffic lights, rrCross)
# allow for the switch to maintenance mode, which will then push the changes in switch state to the main
# there are 2 buttons, one to switch to maintenance mode, the other to toggle switch pos. can only toggle in maintenance

import os
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

import pyfirmata2
import time
board = pyfirmata2.ArduinoMega('COM3')

# Vars
switches = []
blocks = []
rrCrossing = []
trafficLights = []
mode = 0
modeButtonPressed = True
switchButtonPressed = True

current_dir = os.path.dirname(__file__)  # setting up dir to work in any location in a directory
hw_subdir = os.path.join(os.path.dirname(__file__), 'HWUIData')
hw_subdir = 'HWUIData'
hw_subfolder = os.path.join(current_dir, hw_subdir)

# Library of Pins:
bl1 = board.get_pin('d:28:o')
bl2 = board.get_pin('d:29:o')
bl3 = board.get_pin('d:31:o')
bl4 = board.get_pin('d:32:o')
bl5 = board.get_pin('d:33:o')
bl6 = board.get_pin('d:23:o')
bl7 = board.get_pin('d:24:o')
bl8 = board.get_pin('d:25:o')
bl9 = board.get_pin('d:26:o')
bl10 = board.get_pin('d:27:o')
bl11 = board.get_pin('d:35:o')
bl12 = board.get_pin('d:36:o')
bl13 = board.get_pin('d:37:o')
bl14 = board.get_pin('d:38:o')
bl15 = board.get_pin('d:39:o')
swL = board.get_pin('d:22:o')
swR = board.get_pin('d:34:o')
rrC1 = board.get_pin('d:30:o')

swMode = board.get_pin('a:0:i')
swFlip = board.get_pin('a:1:i')

hex1 = board.get_pin('d:2:o')
hex2 = board.get_pin('d:3:o')
hex3 = board.get_pin('d:4:o')
hex4 = board.get_pin('d:5:o')
hex5 = board.get_pin('d:6:o')
hex6 = board.get_pin('d:7:o')
hex7 = board.get_pin('d:8:o')


hex1.write(0)
hex2.write(0)
hex3.write(0)
hex4.write(1)
hex5.write(0)
hex6.write(0)
hex7.write(0)


def flip_switch(value):  # each time data is sent to board, checks for a valid range of button press then change sw state
    global switchButtonPressed
    val = swFlip.read()
    if val >= 1 and mode == 1:  # check for valid button press
        if not switchButtonPressed:
            switchButtonPressed = True
            global switches
            if switches[0] == 'R':
                switches[0] = 'L'
                send_to_main()
            else:
                switches[0] = 'R'
                send_to_main()
            time.sleep(.8)  # debounce
    else:
        switchButtonPressed = False


def mode_switch(value):  # each time data is sent to board, checks for a valid range of button press then updates mode
    global modeButtonPressed
    val = swMode.read()
    if val >= 1:  # check for valid button press
        if not modeButtonPressed:
            modeButtonPressed = True
            global mode
            if mode == 0:
                mode = 1
                send_to_main()
            else:
                mode = 0
                send_to_main()
            time.sleep(.8)  # debounce
    else:
        modeButtonPressed = False


board.samplingOn(500)
swMode.register_callback(mode_switch)
swFlip.register_callback(flip_switch)

#swMode.enable_reporting()
#swMode.mode = pyfirmata2.INPUT
#it = pyfirmata2.util.Iterator(board)
#it.start()


class HWUI(FileSystemEventHandler):  # watchdog behavior for the TB data

    def on_modified(self, event):
        self.assign_hw_data()
        self.show_hw_data()

    def assign_hw_data(self):
        global switches
        global blocks
        global rrCrossing
        global trafficLights
        global mode

        path = os.path.join(hw_subfolder, 'HWData.txt')

        with open(path, 'r') as file:
            # Read the contents of the file
            data = file.read()

        # Evaluate the contents of the file as Python code
        try:
            exec(data, globals())
        except Exception as e:
            print("Error occurred while assigning data:", e)


    def show_hw_data(self):  # reads current vars and assigns those pins to the board

        binblocks = [1 if block == 'O' else 0 for block in blocks]
        binswitches = [1 if switch == 'R' else 0 for switch in switches]

        bl1.write(binblocks[0])
        bl2.write(binblocks[1])
        bl3.write(binblocks[2])
        bl4.write(binblocks[3])
        bl5.write(binblocks[4])
        bl6.write(binblocks[5])
        bl7.write(binblocks[6])
        bl8.write(binblocks[7])
        bl9.write(binblocks[8])
        bl10.write(binblocks[9])
        bl11.write(binblocks[10])
        bl12.write(binblocks[11])
        bl13.write(binblocks[12])
        bl14.write(binblocks[13])
        bl15.write(binblocks[14])

        if rrCrossing == 1:
            rrC1.write(1)
        else:
            rrC1.write(0)

        for i in range(0, len(switches)):
            if binswitches[i] == 1:
                swR.write(1)
                swL.write(0)
            else:
                swR.write(0)
                swL.write(1)

        if mode == 0:  # "A" for auto
            hex1.write(0)
            hex2.write(0)
            hex3.write(0)
            hex4.write(1)
            hex5.write(0)
            hex6.write(0)
            hex7.write(0)
        else:  # "m" for maintenance
            hex1.write(1)
            hex2.write(0)
            hex3.write(1)
            hex4.write(0)
            hex5.write(0)
            hex6.write(0)
            hex7.write(0)


def send_to_main():  # pushes the displayable data to the txt file that the main module is watching
    with open(os.path.join(hw_subfolder, 'HWData.txt'), 'w') as file:
        file.write(f"switches = {switches}\n")
        file.write(f"blocks = {blocks}\n")
        file.write(f"rrCrossing = {rrCrossing}\n")
        file.write(f"trafficLights = {trafficLights}\n")
        file.write(f"mode = {mode}\n")



HW_handler = HWUI()  # Setting up watchdog for Hardware
HWObserver = Observer()
HWObserver.schedule(HW_handler, hw_subfolder, recursive=True)
HWObserver.start()



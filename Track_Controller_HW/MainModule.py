# This is the Main Module.
# This receives data from the tbHandler, the CTC module, the track model, the hardware UI, and the PLC
# Author: Devin James
# 2/17/2024

# Functions:
# send data to the track model
# receive data from the CTC
# load the PLC file, accept the data changes and update its variables
# send variables to the Hardware UI to be displayed
# accepts changes in values from the Hardware UI and the tbHandler
# uses watchdog interrupts to update its values automatically whenever the PLC, Test Bench, or HardwareUI makes changes

import time
import os
import sys
import HardwareUI
import TestBench
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

# Global vars allowing for easier access for the watchdog handlers to reassign vals
mode = 0
authority = 0
numSwitches = 1
numBlocks = 15
switches = ['L'] * numSwitches
blocks = ['E'] * numBlocks
suggestedSpeed = 0.0
rrCrossing = [0]
trafficLights = [0] * numSwitches

# Watchdog setup
currentDir = os.path.dirname(__file__)  # setting up dir to work in any location in a directory

PLCPath = ''  # updated at import time
PLCDataFilePath = 'F:/PLC/PLCData/PLCData.txt'

HWsubdir = 'HWUIData'
HWsubfolder = os.path.join(currentDir, HWsubdir)

TBsubdir = 'TBData'
TBsubfolder = os.path.join(currentDir, TBsubdir)


def PLCimport():  # guarded import of PLC, checking for existence in a specified folder of a USB drive
    print("running PLC import wizard...")
    path = 'F:/PLC'
    file = 'PLCProgram.py'

    try:  # guarded import of PLC prog
        if os.path.exists(path):
            fullpath = os.path.join(path, file)  # found a drive!
            if os.path.isfile(fullpath):
                print("Found the PLC file!")  # found the file! imported
                global PLCPath
                PLCPath = path  # Location of PLCProgram

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


class TBDataHandler(FileSystemEventHandler):  # watchdog behavior for the TB data

    def on_modified(self, event):
        self.assignTBData()
        dispData()

    def assignTBData(self):  # updates the global vars with the values read from the TBData file
        global switches
        global blocks
        global authority
        global suggestedSpeed
        global mode

        path = os.path.join(TBsubfolder, 'TBData.txt')  # path to the data file coming from the Test Bench

        with open(path, 'r') as file:
            # Read the contents of the file
            lines = file.readlines()

            # Check if there are any lines in the file
            if lines:
                # If there are lines, process them
                for line in lines:
                    # Split the line by '='
                    parts = line.split('=')
                    if len(parts) == 2:
                        key = parts[0].strip()
                        value = parts[1].strip()

                        # Assign values based on keys
                        if key == 'switches':
                            # Check if value is a list or a single value
                            if '[' in value and ']' in value:
                                switches = eval(value)
                            else:
                                switches = [eval(value)]  # Convert single value to list
                        elif key == 'blocks':
                            blocks = eval(value)
                        elif key == 'suggestedSpeed':
                            suggestedSpeed = eval(value)
                        elif key == 'authority':
                            authority = eval(value)
                        elif key == 'mode':
                            mode = eval(value)


class mainHWHandler(FileSystemEventHandler):  # watchdog behavior for the TB data

    def on_modified(self, event):
        self.assignHWData()

    def assignHWData(self):  # updates the global vars with the values read from the TBData file
        global switches
        global blocks
        global rrCrossing
        global trafficLights
        global mode

        path = os.path.join(HWsubfolder, 'HWData.txt')  # path to the data file coming from the Test Bench

        with open(path, 'r') as file:
            # Read the contents of the file
            lines = file.readlines()

            # Check if there are any lines in the file
            if lines:
                # If there are lines, process them
                for line in lines:
                    # Split the line by '='
                    parts = line.split('=')
                    if len(parts) == 2:
                        key = parts[0].strip()
                        value = parts[1].strip()

                        # Assign values based on keys
                        if key == 'switches':
                            # Check if value is a list or a single value
                            if '[' in value and ']' in value:
                                switches = eval(value)
                            else:
                                switches = [eval(value)]  # Convert single value to list
                        elif key == 'blocks':
                            blocks = eval(value)
                        elif key == 'rrCrossing':
                            rrCrossing = eval(value)
                        elif key == 'trafficLights':
                            trafficLights = eval(value)
                        elif key == 'mode':
                            mode = eval(value)


class MainModule:
    def sendToHw(self):  # pushes the displayable data to the txt file that the HW module is watching

        with open(os.path.join(HWsubfolder, 'HWData.txt'), 'w') as file:
            file.write(f"switches = {switches}\n")
            file.write(f"blocks = {blocks}\n")
            file.write(f"rrCrossing = {rrCrossing}\n")
            file.write(f"trafficLights = {trafficLights}\n")
            # file.write(f"mode = {mode}\n")

    def sendToTrack(self):  # pushing values to the track model
        return authority, suggestedSpeed, switches, blocks, rrCrossing, trafficLights

def dispData():  # displays current data values
    print("-----------------")
    print("BLOCK STATUS:")
    print("Blocks:", blocks)
    print("-----------------")
    print("SWITCH STATUS:")
    print("Switches:", switches)
    print("-----------------")
    print("AUTHORITY:")
    print("Authority:", authority, " blocks")
    print("-----------------")
    print("SUGGESTED SPEED:")
    print("Suggested Speed:", suggestedSpeed, " m/s")
    print("-----------------")
    print("MODE:")
    print("Mode: ", mode)
    print("-----------------")
    print("RRCROSSING:")
    print("RR crossing: ", rrCrossing)
    print("-----------------")
    print("\n\n")

if __name__ == "__main__":

    TB_handler = TBDataHandler()  # Setting up watchdog for Test Bench
    TBObserver = Observer()
    TBObserver.schedule(TB_handler, TBsubfolder, recursive=False)
    TBObserver.start()

    mainHW_handler = mainHWHandler()  # Setting up watchdog for Hardware
    mainHWObserver = Observer()
    mainHWObserver.schedule(mainHW_handler, HWsubfolder, recursive=False)
    mainHWObserver.start()

    mainMod = MainModule()

    choice = input("1 for dummySim, 2 for test bench\n")

    if choice == '1':
        # DUMMYSIM
        PLCimport()  # importing PLC (or exiting if it is not present in a USB)
        sys.path.append(PLCPath)
        import PLCProgram

        trainLoc = 0  # starting location for train
        plc = PLCProgram.PLC()

        while True:

            binSwitches = [True if switch == 'R' else False for switch in switches]  # to maintain boolean vars for PLC
            binBlocks = [True if block == 'O' else False for block in blocks]

            plc.assignPLCData(rrCrossing, trafficLights, binSwitches, binBlocks, mode)  # sending curr vals to PLC for logic
            plc.runPLCLogic()  # run the logic with the vals passed in
            rrCrossing, trafficLights, binSwitches = plc.PLCToMain()  # assigning the values spat out by PLC logic

            switches = ['R' if switch else 'L' for switch in binSwitches]  # updating switches based on binSwitches
            mainMod.sendToHw()  # updating the UI

            time.sleep(.5)

            # "Train" movement
            for i in range(len(blocks)):  # resetting past occupancy and updating
                blocks[i] = 'E'
            blocks[trainLoc] = 'O'

            if trainLoc == 14 or trainLoc == 9:  # checking to see if train is at the end of the track
                trainLoc = 0
            else:
                trainLoc += 1

            if trainLoc == 5 and switches[0] == 'R':  # path that the train takes based on switch position
                trainLoc = 10
            elif trainLoc == 5 and switches[0] == 'L':
                trainLoc = 5
    else:
        TestBench.runTB()
        while True:
            mainMod.sendToHw()
            time.sleep(.2)


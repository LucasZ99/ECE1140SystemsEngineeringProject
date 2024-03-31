# This is the Main Module.
# This receives data from the tbHandler, the CTC module, the track model, the hardware UI, and the PLC
# Author: Devin James
# 2/29/2024

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
num_switches = 1
num_blocks = 15
switches = ['L'] * num_switches
blocks = ['E'] * num_blocks
suggested_speed = 0.0
rr_crossing = [0]
traffic_lights = [0] * num_switches

# Watchdog setup
current_dir = os.path.dirname(__file__)  # setting up dir to work in any location in a directory

plc_path = ''  # updated at import time
plc_data_file_path = 'F:/PLC/PLCData/PLCData.txt'

hw_subdir = 'HWUIData'
hw_subfolder = os.path.join(current_dir, hw_subdir)

tb_subdir = 'TBData'
tb_subfolder = os.path.join(current_dir, tb_subdir)


def plc_import():  # guarded import of PLC, checking for existence in a specified folder of a USB drive
    print("running PLC import wizard...")
    path = 'F:/PLC'
    file = 'PLCProgram.py'

    try:  # guarded import of PLC prog
        if os.path.exists(path):
            fullpath = os.path.join(path, file)  # found a drive!
            if os.path.isfile(fullpath):
                print("Found the PLC file!")  # found the file! imported
                global plc_path
                plc_path = path  # Location of PLCProgram

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


class tb_data_handler(FileSystemEventHandler):  # watchdog behavior for the TB data

    def on_modified(self, event):
        self.assign_tb_data()
        disp_data()

    def assign_tb_data(self):  # updates the global vars with the values read from the TBData file
        global switches
        global blocks
        global authority
        global suggested_speed
        global mode

        path = os.path.join(tb_subfolder, 'TBData.txt')  # path to the data file coming from the Test Bench

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
                        elif key == 'rr_crossing':
                            rr_crossing = eval(value)
                        elif key == 'traffic_lights':
                            traffic_lights = eval(value)
                        elif key == 'mode':
                            mode = eval(value)


class main_hw_handler(FileSystemEventHandler):  # watchdog behavior for the TB data

    def on_modified(self, event):
        self.assign_hw_data()

    def assign_hw_data(self):  # updates the global vars with the values read from the TBData file
        global switches
        global blocks
        global rr_crossing
        global traffic_lights
        global mode

        path = os.path.join(hw_subfolder, 'HWData.txt')  # path to the data file coming from the Test Bench

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
                        elif key == 'rr_crossing':
                            rr_crossing = eval(value)
                        elif key == 'traffic_lights':
                            traffic_lights = eval(value)
                        elif key == 'mode':
                            mode = eval(value)


class track_controller:
    def send_to_hw(self):  # pushes the displayable data to the txt file that the HW module is watching

        with open(os.path.join(hw_subfolder, 'HWData.txt'), 'w') as file:
            file.write(f"switches = {switches}\n")
            file.write(f"blocks = {blocks}\n")
            file.write(f"rr_crossing = {rr_crossing}\n")
            file.write(f"traffic_lights = {traffic_lights}\n")
            # file.write(f"mode = {mode}\n")

    def sendToTrack(self):  # pushing values to the track model
        return authority, suggested_speed, switches, blocks, rr_crossing, traffic_lights

def disp_data():  # displays current data values
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
    print("Suggested Speed:", suggested_speed, " m/s")
    print("-----------------")
    print("MODE:")
    print("Mode: ", mode)
    print("-----------------")
    print("rr_crossing:")
    print("RR crossing: ", rr_crossing)
    print("-----------------")
    print("\n\n")

if __name__ == "__main__":

    TB_handler = tb_data_handler()  # Setting up watchdog for Test Bench
    TBObserver = Observer()
    TBObserver.schedule(TB_handler, tb_subfolder, recursive=False)
    TBObserver.start()

    mainHW_handler = main_hw_handler()  # Setting up watchdog for Hardware
    mainHWObserver = Observer()
    mainHWObserver.schedule(mainHW_handler, hw_subfolder, recursive=False)
    mainHWObserver.start()

    mainMod = track_controller()

    choice = input("1 for dummySim, 2 for test bench\n")

    if choice == '1':
        # DUMMYSIM
        plc_import()  # importing PLC (or exiting if it is not present in a USB)
        sys.path.append(plc_path)
        import PLCProgram

        trainLoc = 0  # starting location for train
        plc = PLCProgram.PLC()

        while True:

            binSwitches = [True if switch == 'R' else False for switch in switches]  # to maintain boolean vars for PLC
            binBlocks = [True if block == 'O' else False for block in blocks]

            plc.assign_plc_data(rr_crossing, traffic_lights, binSwitches, binBlocks, mode)  # sending curr vals to PLC for logic
            plc.run_plc_logic()  # run the logic with the vals passed in
            rr_crossing, traffic_lights, binSwitches = plc.plc_to_main()  # assigning the values spat out by PLC logic

            switches = ['R' if switch else 'L' for switch in binSwitches]  # updating switches based on binSwitches
            mainMod.send_to_hw()  # updating the UI

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
        TestBench.run_tb()
        while True:
            mainMod.send_to_hw()
            time.sleep(.2)


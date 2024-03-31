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
import socket
import time
serverAddress = ('192.168.1.184', 2222)
bufferSize = 1024
UDPClient = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Vars
switches = []
blocks = []
rrCrossing = []
trafficLights = []
mode = False
modeButtonPressed = True
switchButtonPressed = True

current_dir = os.path.dirname(__file__)  # setting up dir to work in any location in a directory
hw_subdir = os.path.join(os.path.dirname(__file__), 'HWUIData')
hw_subfolder = os.path.join(current_dir, hw_subdir)


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


    def show_hw_data(self):  # send data through server to Pi
        block_send = ''.join(map(str, map(int, blocks)))
        block = block_send.encode('utf-8')

        UDPClient.sendto(block, serverAddress)


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
print("HW started")



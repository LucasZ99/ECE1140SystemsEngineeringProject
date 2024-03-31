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
import socket
import time
serverAddress = ('192.168.1.184', 2222)
bufferSize = 1024
UDPClient = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
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



class HWUI():  # watchdog behavior for the TB data

    def on_modified(self, event):
        self.assign_hw_data()
        self.show_hw_data()

    def assign_hw_data(self):
        global switches
        global blocks
        global rrCrossing
        global trafficLights
        global mode



    def show_hw_data(self):  # send data through server to Pi
        block_send = ''.join(map(str, map(int, blocks)))
        block = block_send.encode('utf-8')

        UDPClient.sendto(block, serverAddress)


def send_to_main():  # pushes the displayable data to the txt file that the main module is watching



    print("HW started")



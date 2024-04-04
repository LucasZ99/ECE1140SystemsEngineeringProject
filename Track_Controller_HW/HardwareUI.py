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


class HWUI:
    def __init__(self):  # create connection to server
        self.serverAddress = ('192.168.1.184', 2222)
        self.bufferSize = 1024
        self.UDPClient = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        print("Track Controller HW UI started...")

    def show_hw_data(self, blocks, mode, rr_cross, switches):  # send data through server to Pi
        data_to_send = ''.join('1' if block else '0' for block in blocks)
        data_to_send += '1' if mode else '0'  # Represent mode
        data_to_send += '1' if rr_cross else '0'  # Represent rr_cross
        data_to_send += '1' if switches else '0'  # Represent switches
        self.UDPClient.sendto(data_to_send.encode('utf-8'), self.serverAddress)
        print("Data sent to Pi")


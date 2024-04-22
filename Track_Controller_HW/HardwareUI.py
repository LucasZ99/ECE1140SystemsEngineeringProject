# This is the Hardware UI.
# This receives data from the Main Module, for the purpose of display
# also has a switch to enable maintenance mode, which will allow the manual flipping of switches
# Author: Devin James
# 2/17/2024


import os
import socket
import time
import json


class HWUI:
    data_to_send = {}
    def __init__(self):  # create connection to server
        self.serverAddress = ('192.168.1.184', 2222)
        self.bufferSize = 3072
        self.UDPClient = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        print("WS HW: Track Controller HW UI started...")

    def show_hw_data(self, blocks, mode, rr_cross, zero_speed):  # send data through server to Pi
        self.data_to_send = {
            "blocks": blocks,
            "mode": mode,
            "rr_cross": rr_cross,
            "zero_speed": zero_speed
        }

        json_string = json.dumps(self.data_to_send)
        #print (json_string)
        self.UDPClient.sendto(json_string.encode('utf-8'), self.serverAddress)
        print("WS HW: Data sent to Pi")


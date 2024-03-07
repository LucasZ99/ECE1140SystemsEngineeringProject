# This is the hardware track controller module.
# Author: Devin James
# 2/14/2024

import time
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer
import os

# Global Variables
authority = 5
suggestedSpeed = 50
numSwitches = 1
numBlocks = 15
switches = ['L'] * numSwitches
blocks = ['E'] * numBlocks

path = 'C:/Users/18dja/Documents/Homework/ECE Trains/Test Bench UI/Data'

class tBHandler(FileSystemEventHandler):
    def on_modified(self, event):
        print("Test Bench data was modified.")
        assignTBData()
        dispTBData()


def dispTBData():  # receives the data from the testBench
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


def assignTBData():  # Read data from txt file and assign to variables
    global switches
    global blocks
    global authority
    global suggestedSpeed

    with open('C:/Users/18dja/Documents/Homework/ECE Trains/Test Bench UI/Data/TBData.txt', 'r') as file:
        # Read the contents of the file
        lines = file.readlines()

        # Assign the values to variables
        authority = int(lines[0].split('=')[1].strip())
        suggestedSpeed = float(lines[1].split('=')[1].strip())
        switches = eval(lines[2].split('=')[1].strip())  # Use eval to convert string representation of list to list
        blocks = eval(lines[3].split('=')[1].strip())  # Use eval to convert string representation of list to list


if __name__ == "__main__":
    event_handler = tBHandler()  # Setting up watchdog
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()

    while True:
        time.sleep(1)

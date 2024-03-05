from PyQt6.QtCore import QObject

from Track_Controller_SW.switching import Switch

import subprocess


class PlcProgram(QObject):
    def __init__(self):
        super().__init__()
        self.filepath = None

    def set_filepath(self, filepath: str):
        self.filepath = filepath
        print(f"filepath: {self.filepath}")

    def execute_plc(self, occupancy_list: list[bool] = None, switches_list: list[Switch] = None, block_to_close: int = None):
        safe_speed, switch_permitted, close_block_permitted = (
            subprocess.run(['python', self.filepath, occupancy_list, switches_list, block_to_close]).returncode)
        return safe_speed, switch_permitted, close_block_permitted

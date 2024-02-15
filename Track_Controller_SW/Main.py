from PyQt5.QtWidgets import QApplication
import sys
import tc_ui
import switching
import PLC_Logic

class track_controller():
    def __init__(self, switches_arr, plc_logic, block_occupancy, authority):
        self.switches_arr = switches_arr
        self.plc_logic = plc_logic
        self.block_occupancy = block_occupancy
        self.authority = authority
        self.UI = tc_ui.UI(switches_arr, plc_logic, block_occupancy, authority)


if __name__ == "__main__":
    switches_arr = [switching.switch(5, 6, 11, 6), switching.switch(6, 7, 8, 7)]
    plc_logic = PLC_Logic.parse_plc()
    block_occupancy = [False] * 15
    authority = None
    app = QApplication(sys.argv)
    UI = tc_ui.UI(switches_arr, plc_logic, block_occupancy, authority)
    UI.show()
    app.exec()





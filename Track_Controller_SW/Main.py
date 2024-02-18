from PyQt6.QtWidgets import QApplication
import sys
import tc_ui
import switching
import PLC_Logic
import BusinessObject


class TrackController(object):
    def __init__(self, switches_arr, plc_logic, authority, business_logic):
        self.switches_arr = switches_arr
        self.plc_logic = plc_logic
        self.block_occupancy = block_occupancy
        self.authority = authority
        self.UI = tc_ui.UI(switches_arr, plc_logic, authority, business_logic)


if __name__ == "__main__":
    switches_arr = [switching.Switch(5, 6, 11, 6)]
    plc_logic = PLC_Logic.ParsePlc()
    block_occupancy = [False] * 15
    business_logic = BusinessObject.BusinessLogic(block_occupancy, switches_arr)
    authority = None
    app = QApplication(sys.argv)
    UI = tc_ui.UI(plc_logic, authority, business_logic)
    UI.show()
    app.exec()

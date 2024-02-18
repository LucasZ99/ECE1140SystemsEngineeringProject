import sys

from PyQt6.QtWidgets import QApplication

import BusinessObject
import PLC_Logic
import switching
import tc_ui


def main():
    switches_arr = [switching.Switch(5, 6, 11, 6)]
    plc_logic = PLC_Logic.ParsePlc()
    block_occupancy = [False] * 16
    authority = True
    suggested_speed = 0.0
    business_logic = BusinessObject.BusinessLogic(block_occupancy, switches_arr, authority, suggested_speed)
    app = QApplication(sys.argv)
    ui = tc_ui.UI(plc_logic, business_logic)
    ui.show()
    app.exec()


if __name__ == "__main__":
    main()

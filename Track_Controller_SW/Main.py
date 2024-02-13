import tc_ui
import switching
import PLC_Logic
import TestBench
class track_controller():
    def __init__(self, switches_arr, plc_logic, block_occupancy, authority):
        self.switches_arr = switches_arr
        self.plc_logic = plc_logic
        self.block_occupancy = block_occupancy
        self.authority = authority
        self.UI = tc_ui.main(switches_arr, plc_logic)
        self.tb = TestBench.main(block_occupancy, authority)


if __name__ == "__main__":
    switches_arr = [switching.switch(5, 6, 11, 6)]
    plc_logic = PLC_Logic.parse_plc()
    block_occupancy = []
    authority = None
    tc = track_controller(switches_arr, plc_logic, block_occupancy, authority)





from PyQt6.QtCore import QObject, pyqtSignal
from PyQt6.QtCore import pyqtSlot

from Track_Controller_SW.PLC_Logic import PlcProgram


class BusinessLogic(QObject):
    # Define Signals
    occupancy_signal = pyqtSignal(list)
    switches_signal = pyqtSignal(list)
    rr_crossing_signal = pyqtSignal(bool)
    light_signal = pyqtSignal(int)

    def __init__(self, block_occupancy: list, switches_arr: list, authority: int, suggested_speed: float, plc_logic: PlcProgram):
        super().__init__()
        self.occupancy_list = block_occupancy
        self.switches_list = switches_arr
        self.authority = authority
        self.suggested_speed = suggested_speed
        self.plc_logic = plc_logic

    # Must call this method whenever occupancy is updated
    @pyqtSlot(list)
    def occupancy_changed(self, new_occupancy: list) -> None:
        print("Occupancy changed")
        self.occupancy_list = new_occupancy
        if new_occupancy[3] is True:
            self.rr_crossing_signal.emit(True)
        else:
            self.rr_crossing_signal.emit(False)
        self.occupancy_signal.emit(self.occupancy_list)

    @pyqtSlot(int)
    def switches_changed(self, index: int) -> None:
        print(f"Switch at b{self.switches_list[index].block} changed")
        self.switches_list[index].toggle()
        if self.switches_list[index].current_pos == self.switches_list[index].pos_a:
            self.light_signal.emit(self.switches_list[index].pos_a)
        else:
            self.light_signal.emit(self.switches_list[index].pos_b)

        self.switches_signal.emit(self.switches_list)

    # TODO: this is currently a placeholder for business logic on the authority
    @pyqtSlot(bool)
    def authority_updated(self, block: int, is_authority: bool) -> None:
        print(f"Authority updated to {int(is_authority)}")

    @pyqtSlot(float)
    def sug_speed_updated(self, sug_speed: float) -> None:
        print(f"Suggested speed updated to {sug_speed}")

    def set_plc_filepath(self, plc_filepath: str) -> None:
        self.plc_logic.set_filepath(plc_filepath)

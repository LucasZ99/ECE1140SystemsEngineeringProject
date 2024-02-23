from PyQt6.QtCore import QObject, pyqtSignal
from PyQt6.QtCore import pyqtSlot


class BusinessLogic(QObject):
    # Define Signals
    occupancy_signal = pyqtSignal(list)
    switches_signal = pyqtSignal(list)
    rr_crossing_signal = pyqtSignal(bool)
    light_signal = pyqtSignal(int)

    def __init__(self, block_occupancy, switches_arr, authority, suggested_speed):
        super().__init__()
        self.occupancy_arr = block_occupancy
        self.switches_arr = switches_arr
        self.authority = authority
        self.suggested_speed = suggested_speed

    # Must call this method whenever occupancy is updated
    @pyqtSlot(list)
    def occupancy_changed(self, new_occupancy):
        print("Occupancy changed")
        self.occupancy_arr = new_occupancy
        if new_occupancy[3] is True:
            self.rr_crossing_signal.emit(True)
        else:
            self.rr_crossing_signal.emit(False)
        self.occupancy_signal.emit(self.occupancy_arr)

    @pyqtSlot(int)
    def switches_changed(self, index):
        print(f"Switch at b{self.switches_arr[index].block} changed")
        self.switches_arr[index].toggle()
        if self.switches_arr[index].current_pos == self.switches_arr[index].pos_a:
            self.light_signal.emit(self.switches_arr[index].pos_a)
        else:
            self.light_signal.emit(self.switches_arr[index].pos_b)

        self.switches_signal.emit(self.switches_arr)

    # TODO: this is currently a placeholder for business logic on the authority
    @pyqtSlot(bool)
    def authority_updated(self, is_authority):
        print(f"Authority updated to {int(is_authority)}")

    @pyqtSlot(float)
    def sug_speed_updated(self, sug_speed):
        print(f"Suggested speed updated to {sug_speed}")

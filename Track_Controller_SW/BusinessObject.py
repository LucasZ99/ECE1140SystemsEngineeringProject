from PyQt6.QtCore import QObject, pyqtSlot
from PyQt6.QtCore import QObject, pyqtSignal


class BusinessLogic(QObject):
    # Define Signals
    occupancy_signal = pyqtSignal(list)
    switches_signal = pyqtSignal(list)

    def __init__(self, block_occupancy, switches_arr):
        super().__init__()
        self.occupancy_arr = block_occupancy
        self.switches_arr = switches_arr

    # Must call this method whenever occupancy is updated
    @pyqtSlot(list)
    def occupancy_changed(self, new_occupancy):
        print("Occupancy changed")
        self.occupancy_arr = new_occupancy
        self.occupancy_signal.emit(self.occupancy_arr)

    @pyqtSlot(int)
    def switches_changed(self, index):
        print("Switches changed")
        self.switches_arr[index].toggle()
        self.switches_signal.emit(self.switches_arr)






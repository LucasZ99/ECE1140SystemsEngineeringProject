from PyQt6.QtCore import QObject, pyqtSignal

from Common.TrackSignal import TrackSignal


class TestBusinessLogic(QObject):

    ctc_inputs_from_testbench_signal = pyqtSignal(list)
    track_inputs_from_testbench_signal = pyqtSignal(dict)

    def __init__(self):
        super().__init__()
        self.track_signal = TrackSignal(0, 0, 0)
        self.occupancy_dict = {}
        # Add values from 1 to 57
        for i in range(1, 58):
            self.occupancy_dict[i] = False
        for i in range(62, 151):
            self.occupancy_dict[i] = False

        self.blocks = list(self.occupancy_dict.keys())

    def track_signal_authority_update(self, authority: int):
        self.track_signal.authority = authority

    def occupancy_update(self, blocks_occupancy: dict[int, bool]):
        self.occupancy_dict = blocks_occupancy

    def track_signal_block_update(self, block: int):
        self.track_signal.block_id = block

    def track_signal_speed_update(self, speed: float):
        self.track_signal.speed = speed

    def send_ctc_inputs(self):
        if self.track_signal.block_id != 0:
            self.ctc_inputs_from_testbench_signal.emit([self.track_signal])

    def send_track_inputs(self):
        self.track_inputs_from_testbench_signal.emit(self.occupancy_dict)



from PyQt6.QtCore import QObject, pyqtSignal, pyqtSlot

from Common import Switch
from Common.TrackSignal import TrackSignal
from TrackControllerTest.TrackControllerTestSignals import TrackControllerTestSignals as signals


class TestBackend(QObject):

    def __init__(self):
        super().__init__()
        self.signals = signals
        self.track_signal = TrackSignal(1, 0, 0)
        self.occupancy_dict = {}
        # Add values from 1 to 57
        for i in range(1, 58):
            self.occupancy_dict[i] = False
        for i in range(62, 151):
            self.occupancy_dict[i] = False

        self.switch_list = \
            [
                Switch(13, 12, 1, 12),
                Switch(28, 29, 150, 29),
                Switch(77, 76, 101, 76),
                Switch(85, 86, 100, 86)
            ]

        self.blocks = list(self.occupancy_dict.keys())
        self.block_to_toggle = [[0, True]]
        self.switch_to_toggle = []

        # connect external signals
        self.signals.get_blocks_signal.connect(self.send_blocks)
        self.signals.get_blocks_occupancy_signal.connect(self.send_blocks_occupancy)
        self.signals.track_signal_authority_update_signal.connect(self.track_signal_authority_update)
        self.signals.occupancy_update_signal.connect(self.occupancy_update)
        self.signals.track_signal_block_update_signal.connect(self.track_signal_block_update)
        self.signals.track_signal_speed_update_signal.connect(self.track_signal_speed_update)
        self.signals.send_ctc_inputs_signal.connect(self.send_ctc_inputs)
        self.signals.send_track_inputs_signal.connect(self.send_track_inputs)
        self.signals.block_to_toggle.connect(self.toggle_block_update)
        self.signals.get_switches_signal.connect(self.send_switches)
        self.signals.switch_to_toggle.connect(self.toggle_switch_update)

    def toggle_switch_update(self, switch: Switch):
        if len(self.switch_to_toggle) > 0:
            self.switch_to_toggle[0] = switch
        else:
            self.switch_to_toggle.append(switch)

    def send_switches(self):
        self.signals.send_switches_signal.emit(self.switch_list)

    @pyqtSlot(int)
    def toggle_block_update(self, block_index: int):

        if self.block_to_toggle[0][0] == block_index:
            self.block_to_toggle[0] = [block_index, True]
        else:
            self.block_to_toggle[0] = [block_index, False]

    @pyqtSlot()
    def send_blocks_occupancy(self):
        self.signals.send_blocks_occupancy_signal.emit(self.occupancy_dict)

    @pyqtSlot()
    def send_blocks(self):
        self.signals.send_blocks_signal.emit(self.blocks)

    @pyqtSlot(int)
    def track_signal_authority_update(self, authority: int):
        print(f"Authority of track signal: {authority}")
        self.track_signal.authority = authority

    @pyqtSlot(dict)
    def occupancy_update(self, blocks_occupancy: dict[int, bool]):
        self.occupancy_dict = blocks_occupancy

    @pyqtSlot(int)
    def track_signal_block_update(self, block: int):
        print(f"block of track signal: {block}")
        self.track_signal.block_id = block

    @pyqtSlot(float)
    def track_signal_speed_update(self, speed: float):
        print(f"speed of track signal: {speed}")
        self.track_signal.speed = speed

    @pyqtSlot()
    def send_ctc_inputs(self):
        print(f"sending track signal: {self.track_signal}")
        if self.block_to_toggle[0][0] == 0 and len(self.switch_to_toggle) == 0:
            self.signals.ctc_inputs_from_testbench_signal.emit([self.track_signal], [], [])
        elif self.block_to_toggle[0][0] == 0:
            self.signals.ctc_inputs_from_testbench_signal.emit([self.track_signal], [], self.switch_to_toggle)
        elif len(self.switch_to_toggle) == 0:
            self.signals.ctc_inputs_from_testbench_signal.emit([self.track_signal], self.block_to_toggle, [])
        else:
            self.signals.ctc_inputs_from_testbench_signal.emit([self.track_signal], [self.block_to_toggle],
                                                               self.switch_to_toggle)


    @pyqtSlot()
    def send_track_inputs(self):
        print(f"sending occupancy: {self.occupancy_dict}")
        self.signals.track_inputs_from_testbench_signal.emit(self.occupancy_dict)



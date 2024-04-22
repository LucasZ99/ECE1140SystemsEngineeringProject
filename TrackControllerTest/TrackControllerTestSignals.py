from PyQt6.QtCore import QObject, pyqtSignal


class TrackControllerTestSignalsCls(QObject):

    # Get from Business Logic to UI
    get_blocks_signal = pyqtSignal()
    get_blocks_occupancy_signal = pyqtSignal()
    get_switches_signal = pyqtSignal()

    # send from Business Logic to UI
    send_blocks_signal = pyqtSignal(list)
    send_blocks_occupancy_signal = pyqtSignal(dict)
    send_switches_signal = pyqtSignal(list)

    # Send to business logic from UI
    track_signal_authority_update_signal = pyqtSignal(int)
    occupancy_update_signal = pyqtSignal(dict)
    track_signal_block_update_signal = pyqtSignal(int)
    track_signal_speed_update_signal = pyqtSignal(float)
    send_ctc_inputs_signal = pyqtSignal()
    send_track_inputs_signal = pyqtSignal()
    block_to_toggle = pyqtSignal(int)
    switch_to_toggle = pyqtSignal(list)


    # send from business logic to launcher
    ctc_inputs_from_testbench_signal = pyqtSignal(list, list)
    track_inputs_from_testbench_signal = pyqtSignal(dict)

    def __init__(self, parent=None):
        super(TrackControllerTestSignalsCls, self).__init__(parent)


TrackControllerTestSignals = TrackControllerTestSignalsCls()


from PyQt6 import QtCore
from PyQt6.QtCore import QObject, pyqtSignal, pyqtSlot


class CTCTestSignalsCls(QObject):
    # Top Level
    update_ctc_from_wayside = pyqtSignal(dict, list, list, list)
    update_wayside_from_ctc = pyqtSignal(list, list, list)

    # UI and Wayside
    wayside_update_block_occupancy = pyqtSignal(int, bool)
    ui_update_track_signals = pyqtSignal(list)
    ui_update_block_occupancy_signal = pyqtSignal(int, bool)

    wayside_get_track_signals_signal = pyqtSignal()
    wayside_get_occupancies_signal = pyqtSignal()

    def __init__(self):
        super().__init__()
        print("CTC Test Signals Initialized")


CTCTestSignals = CTCTestSignalsCls()

from PyQt6.QtCore import QObject, pyqtSignal


class SystemTimeSignalsCls(QObject):

    # from UI
    multiplier_value_updated_signal = pyqtSignal(float)
    toggle_play_pause_signal = pyqtSignal(bool)

def __init__(self):
    super().__init__()


SystemTimeSignals = SystemTimeSignalsCls()
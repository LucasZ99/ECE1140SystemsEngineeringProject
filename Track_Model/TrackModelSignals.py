from PyQt6.QtCore import pyqtSignal, QObject


class TrackModelSignalsCls(QObject):

    # Track Model -> UI
    refresh_ui_signal = pyqtSignal()
    map_add_train_signal = pyqtSignal()
    map_move_train_signal = pyqtSignal(int, int)
    get_data_signal = pyqtSignal(object)
    get_block_info_signal = pyqtSignal(object)
    get_train_dict_signal = pyqtSignal(dict)
    # UI -> Track Model
    set_power_failure_signal = pyqtSignal(int, bool)
    set_track_circuit_failure_signal = pyqtSignal(int, bool)
    set_broken_rail_failure_signal = pyqtSignal(int, bool)
    set_env_temperature = pyqtSignal(int)
    set_heaters = pyqtSignal(int)

    def __init__(self, parent=None):
        super(TrackModelSignalsCls, self).__init__(parent)


TrackModelSignals = TrackModelSignalsCls()
